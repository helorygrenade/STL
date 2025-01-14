import marimo

__generated_with = "0.9.17"
app = marimo.App()


@app.cell
def __(mo):
    mo.md("""#3D Geometry File Formats""")
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## About STL

        STL is a simple file format which describes 3D objects as a collection of triangles.
        The acronym STL stands for "Simple Triangle Language", "Standard Tesselation Language" or "STereoLitography"[^1].

        [^1]: STL was invented for – and is still widely used – for 3D printing.
        """
    )
    return


@app.cell
def __(mo, show):
    mo.show_code(show("data/teapot.stl", theta=45.0, phi=30.0, scale=2))
    return


@app.cell
def __(mo):
    with open("data/teapot.stl", mode="rt", encoding="utf-8") as _file:
        teapot_stl = _file.read()

    teapot_stl_excerpt = teapot_stl[:723] + "..." + teapot_stl[-366:]

    mo.md(
        f"""
    ## STL ASCII Format

    The `data/teapot.stl` file provides an example of the STL ASCII format. It is quite large (more than 60000 lines) and looks like that:
    """
    +
    f"""```
    {teapot_stl_excerpt}
    ```
    """
    +

    """
    """
    )
    return teapot_stl, teapot_stl_excerpt


@app.cell
def __(mo):
    mo.md(f"""

      - Study the [{mo.icon("mdi:wikipedia")} STL (file format)](https://en.wikipedia.org/wiki/STL_(file_format)) page (or other online references) to become familiar the format.

      - Create a STL ASCII file `"data/cube.stl"` that represents a cube of unit length  
        (💡 in the simplest version, you will need 12 different facets).

      - Display the result with the function `show` (make sure to check different angles).
    """)
    return


@app.cell
def __(show):
    show("data/cube.stl", theta=45.0, phi=30.0, scale=0.5)
    return


@app.cell
def __(mo):
    mo.md(r"""## STL & NumPy""")
    return


@app.cell
def __(mo):
    mo.md(rf"""

    ### NumPy to STL

    Implement the following function:

    ```python
    def make_STL(triangles, normals=None, name=""):
        pass # 🚧 TODO!
    ```

    #### Parameters

      - `triangles` is a NumPy array of shape `(n, 3, 3)` and data type `np.float32`,
         which represents a sequence of `n` triangles (`triangles[i, j, k]` represents 
         is the `k`th coordinate of the `j`th point of the `i`th triangle)

      - `normals` is a NumPy array of shape `(n, 3)` and data type `np.float32`;
         `normals[i]` represents the outer unit normal to the `i`th facet.
         If `normals` is not specified, it should be computed from `triangles` using the 
         [{mo.icon("mdi:wikipedia")} right-hand rule](https://en.wikipedia.org/wiki/Right-hand_rule).

      - `name` is the (optional) solid name embedded in the STL ASCII file.

    #### Returns

      - The STL ASCII description of the solid as a string.

    #### Example

    Given the two triangles that make up a flat square:

    ```python

    square_triangles = np.array(
        [
            [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
            [[1.0, 1.0, 0.0], [0.0, 1.0, 0.0], [1.0, 0.0, 0.0]],
        ],
        dtype=np.float32,
    )
    ```

    then printing `make_STL(square_triangles, name="square")` yields
    ```
    solid square
      facet normal 0.0 0.0 1.0
        outer loop
          vertex 0.0 0.0 0.0
          vertex 1.0 0.0 0.0
          vertex 0.0 1.0 0.0
        endloop
      endfacet
      facet normal 0.0 0.0 1.0
        outer loop
          vertex 1.0 1.0 0.0
          vertex 0.0 1.0 0.0
          vertex 1.0 0.0 0.0
        endloop
      endfacet
    endsolid square
    ```

    """)
    return


@app.cell
def __(np):
    square_triangles = np.array(
        [
            [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
            [[1.0, 1.0, 0.0], [0.0, 1.0, 0.0], [1.0, 0.0, 0.0]],
        ],
        dtype=np.float32,
    )
    return (square_triangles,)


@app.cell
def __(np):
    def vect_prod(v1, v2):
        prod = np.zeros(3)
        prod[0] = v1[1]*v2[2] - v1[2]*v2[1]
        prod[1] = v1[2]*v2[0] - v1[0]*v2[2]
        prod[2] = v1[0]*v2[1] - v1[1]*v2[0]
        return prod
    return (vect_prod,)


@app.cell
def __(np):
    def make_normals(triangles):
        (n, m, p) = triangles.shape
        normals = np.zeros((n, 3), dtype= np.float32)
        for i in range(n):
            normals[i, 0] = np.cross(triangles[i, 1] - triangles[i, 0],triangles[i, 2] - triangles[i, 0])[0]
            normals[i, 1] = np.cross(triangles[i, 1] - triangles[i, 0],triangles[i, 2] - triangles[i, 0])[1]
            normals[i, 2] = np.cross(triangles[i, 1] - triangles[i, 0],triangles[i, 2] - triangles[i, 0])[2]
        return normals
    return (make_normals,)


@app.cell
def __():
    def make_facets(triangle, normal):
        facet = f'\tfacet normal {normal[0]} {normal[1]} {normal[2]}\n'
        facet += '\t\touter loop\n'
        for j in range(3):
            facet += f'\t\tvertex {triangle[j, 0]} {triangle[j, 1]} {triangle[j, 2]}\n'
        facet += '\t\tendloop\n'
        facet += '\tendfacet\n'
        return facet
    return (make_facets,)


@app.cell
def __(make_facets, make_normals):
    def make_stl(triangles, normals = None, name = ''):
        n, m, p = triangles.shape 
        stl_ascii = f'solid {name}\n'
        if normals is None:
            normals = make_normals(triangles)
        for i in range(n):
            stl_ascii += make_facets(triangles[i], normals[i])
        stl_ascii += f'endsolid {name}'
        return stl_ascii
    return (make_stl,)


@app.cell
def __(mo):
    mo.md(
        """
        ### STL to NumPy

        Implement a `tokenize` function


        ```python
        def tokenize(stl):
            pass # 🚧 TODO!
        ```

        that is consistent with the following documentation:


        #### Parameters

          - `stl`: a Python string that represents a STL ASCII model.

        #### Returns

          - `tokens`: a list of STL keywords (`solid`, `facet`, etc.) and `np.float32` numbers.

        #### Example

        For the ASCII representation the square `data/square.stl`, printing the tokens with

        ```python
        with open("data/square.stl", mode="rt", encoding="us-ascii") as square_file:
            square_stl = square_file.read()
        tokens = tokenize(square_stl)
        print(tokens)
        ```

        yields

        ```python
        ['solid', 'square', 'facet', 'normal', np.float32(0.0), np.float32(0.0), np.float32(1.0), 'outer', 'loop', 'vertex', np.float32(0.0), np.float32(0.0), np.float32(0.0), 'vertex', np.float32(1.0), np.float32(0.0), np.float32(0.0), 'vertex', np.float32(0.0), np.float32(1.0), np.float32(0.0), 'endloop', 'endfacet', 'facet', 'normal', np.float32(0.0), np.float32(0.0), np.float32(1.0), 'outer', 'loop', 'vertex', np.float32(1.0), np.float32(1.0), np.float32(0.0), 'vertex', np.float32(0.0), np.float32(1.0), np.float32(0.0), 'vertex', np.float32(1.0), np.float32(0.0), np.float32(0.0), 'endloop', 'endfacet', 'endsolid', 'square']
        ```
        """
    )
    return


@app.cell
def __(np, stl):
    def tokenize(object):
        stl = stl.replace('\t', '').replace('\n', ' ')
        stl = stl.split()
        indices = [i for i, value in enumerate(stl) if (value == 'normal') or (value == 'vertex')]
        for i in indices:
            for k in range(3):
                stl[i + k + 1] = np.float32(stl[i + k + 1])
        return stl
    return (tokenize,)


@app.cell
def __(mo):
    mo.md(
        """
        Implement a `parse` function


        ```python
        def parse(tokens):
            pass # 🚧 TODO!
        ```

        that is consistent with the following documentation:


        #### Parameters

          - `tokens`: a list of tokens

        #### Returns

        A `triangles, normals, name` triple where

          - `triangles`: a `(n, 3, 3)` NumPy array with data type `np.float32`,

          - `normals`: a `(n, 3)` NumPy array with data type `np.float32`,

          - `name`: a Python string.

        #### Example

        For the ASCII representation `square_stl` of the square,
        tokenizing then parsing

        ```python
        with open("data/square.stl", mode="rt", encoding="us-ascii") as square_file:
            square_stl = square_file.read()
        tokens = tokenize(square_stl)
        triangles, normals, name = parse(tokens)
        print(repr(triangles))
        print(repr(normals))
        print(repr(name))
        ```

        yields

        ```python
        array([[[0., 0., 0.],
                [1., 0., 0.],
                [0., 1., 0.]],

               [[1., 1., 0.],
                [0., 1., 0.],
                [1., 0., 0.]]], dtype=float32)
        array([[0., 0., 1.],
               [0., 0., 1.]], dtype=float32)
        'square'
        ```
        """
    )
    return


@app.cell
def __(np):
    def parse(tokens):
        name = ''
        if tokens[1] == tokens[-1]:
            name = tokens[-1]
        ind_norm = [i for i, value in enumerate(tokens) if value == 'normal']
        ind_vertex = [i for i, value in enumerate(tokens) if value == 'vertex']

        n = tokens.count('facet')
        triangles = np.zeros((n,3,3), dtype=np.float32)
        normals = np.zeros((n,3), dtype = np.float32)
        for i in ind_norm:
            normals[ind_norm.index(i)] = np.array(tokens[i+1:i+4])
        for i in ind_vertex[::3]:
            triangles[ind_vertex[::3].index(i)] = np.array([tokens[i+1:i+4], tokens[i+5:i+8], tokens[i+9:i+12]])
        return triangles, normals, name
    return (parse,)


@app.cell
def __(mo):
    mo.md(
        rf"""
    ## Rules & Diagnostics



        Make diagnostic functions that check whether a STL model satisfies the following rules

          - **Positive octant rule.** All vertex coordinates are non-negative.

          - **Orientation rule.** All normals are (approximately) unit vectors and follow the [{mo.icon("mdi:wikipedia")} right-hand rule](https://en.wikipedia.org/wiki/Right-hand_rule).

          - **Shared edge rule.** Each triangle edge appears exactly twice.

          - **Ascending rule.** the z-coordinates of (the barycenter of) each triangle are a non-decreasing sequence.

    When the rule is broken, make sure to display some sensible quantitative measure of the violation (in %).

    For the record, the `data/teapot.STL` file:

      - 🔴 does not obey the positive octant rule,
      - 🟠 almost obeys the orientation rule, 
      - 🟢 obeys the shared edge rule,
      - 🔴 does not obey the ascending rule.

    Check that your `data/cube.stl` file does follow all these rules, or modify it accordingly!

    """
    )
    return


@app.cell
def __():
    def check_positive_octant(triangles, n):
        count = 0
        for i in range(n):
            for j in range(3):
                for k in range(3):
                    if triangles[i, j, k]<0:
                        count += 1
        return (count/(3*n))*100
    return (check_positive_octant,)


@app.cell
def __(np):
    def check_orientation(triangles, normals, n):
        count = 0
        for i in range(n):
            if abs(np.norm(normals([i])) - 1) > 0.1:
                count += 1
                continue
            if np.dot(np.cross(triangles[i,1] - triangles[i,0], triangles[i,2] - triangles[i,0]), normals[i]) != np.norm(np.cross(triangles[i,1] - triangles[i,0], triangles[i,2] - triangles[i,0]))*np.norm(normals[i]):
                count += 1
        return 100*count/n
    return (check_orientation,)


@app.cell
def __():
    def triangle_to_edges(triangle):
    	v0, v1, v2 = map(tuple, triangle)
    	return [tuple(v0, v1), tuple(v1, v2),tuple(v2, v0)]
    return (triangle_to_edges,)


@app.cell
def __(shared_twice, triangle_edges, triangle_to_edges):
    def check_shared_edge(triangles,n):
        edge_count = {}
        for i in range(n):
            triangled_edges = triangle_to_edges(triangles[i])
            for edge in triangle_edges:
                if edge in edge_count:
                    edge_count[edge] +=1
        shared_txice = sum(1 for count in edge_count.values() if count == 2)
        total_edges = len(edge_count)
        return (shared_twice/total_edges)*100
    return (check_shared_edge,)


@app.cell
def __():
    def barycenter_z(triangle):
        v0, v1, v2 = triangle
        return (1/3)*(v0[2]+v1[2]+v2[2])
    return (barycenter_z,)


@app.cell
def __(barycenter_z):
    def check_barycenter_ascending(triangles,n):
        count=0
        for i in range(n):
            if barycenter_z(triangles[i])>barycenter_z(triangles[i+1]):
                count += 1
        return 100*count/n
    return (check_barycenter_ascending,)


@app.cell
def __(
    check_barycenter_ascending,
    check_orientation,
    check_positive_octant,
    check_shared_edge,
    parse,
    tirangles,
    tokenize,
):
    def diagnostic(stl):
        triangles, normals, name = parse(tokenize(stl))
        n=triangles.shape[0]
        positive_percentage = check_positive_octant(triangles, n)
        orientation_percentage = check_orientation(triangles,normals,n)
        shared_edge_percentage = check_shared_edge(tirangles,n)
        ascending_rule_percentage = check_barycenter_ascending(triangles,n)
        print(f'here are the percentage of validity for the following rules for the {name} stl file:\n positive octant rule % = {positive_percentage}\n orientation rule % = {orientation_percentage}\n shared edges rule % = {shared_edge_percentage}\n ascending rule % = {ascending_rule_percentage}')
    return (diagnostic,)


@app.cell
def __(mo):
    mo.md(
    rf"""
    ## OBJ Format

    The OBJ format is an alternative to the STL format that looks like this:

    ```
    # OBJ file format with ext .obj
    # vertex count = 2503
    # face count = 4968
    v -3.4101800e-003 1.3031957e-001 2.1754370e-002
    v -8.1719160e-002 1.5250145e-001 2.9656090e-002
    v -3.0543480e-002 1.2477885e-001 1.0983400e-003
    v -2.4901590e-002 1.1211138e-001 3.7560240e-002
    v -1.8405680e-002 1.7843055e-001 -2.4219580e-002
    ...
    f 2187 2188 2194
    f 2308 2315 2300
    f 2407 2375 2362
    f 2443 2420 2503
    f 2420 2411 2503
    ```

    This content is an excerpt from the `data/bunny.obj` file.

    """
    )
    return


@app.cell
def __(mo, show):
    mo.show_code(show("data/bunny.obj", scale="1.5"))
    return


@app.cell
def __(mo):
    mo.md(
        """
        Study the specification of the OBJ format (search for suitable sources online),
        then develop a `OBJ_to_STL` function that is rich enough to convert the OBJ bunny file into a STL bunny file.
        """
    )
    return


@app.cell
def __(make_stl, np, triangle):
    def OBJ_to_STL(obj):
        list=obj.split('\n')
        list = list[3:]
        list = ' '.join(list)
        list = list.split('f')
        facets = list[1:]
        vertices = list[0].split('v')
        triangles=[]
        for facet in facets:
            facet=facet.split()
            triangle = [vertices[int(triangle[0])], vertices[int(triangle[1])], vertices[int(triangle[2])]]
            triangle_final = []
            for vertex in triangle:
            	triangle_final.append(vertex.split())
            triangles.append(triangle_final)
        return make_stl(np.array(triangles, dtype=np.float32))
    return (OBJ_to_STL,)


@app.cell
def __(mo):
    mo.md(
        rf"""
    ## Binary STL

    Since the STL ASCII format can lead to very large files when there is a large number of facets, there is an alternate, binary version of the STL format which is more compact.

    Read about this variant online, then implement the function

    ```python
    def STL_binary_to_text(stl_filename_in, stl_filename_out):
        pass  # 🚧 TODO!
    ```

    that will convert a binary STL file to a ASCII STL file. Make sure that your function works with the binary `data/dragon.stl` file which is an example of STL binary format.

    💡 The `np.fromfile` function may come in handy.

        """
    )
    return


@app.cell
def __(mo, show):
    mo.show_code(show("data/dragon.stl", theta=75.0, phi=-20.0, scale=1.7))
    return


@app.cell
def __(make_STL, np):
    def STL_binary_to_text(stl_filename_in, stl_filename_out):
        with open(stl_filename_in, mode="rb") as file:
            _ = file.read(80)
            n = np.fromfile(file, dtype=np.uint32, count=1)[0]
            normals = []
            faces = []
            for i in range(n):
                normals.append(np.fromfile(file, dtype=np.float32, count=3))
                faces.append(np.fromfile(file, dtype=np.float32, count=9).reshape(3, 3))
                _ = file.read(2)
        stl_text = make_STL(faces, normals)
        with open(stl_filename_out, mode="w", encoding="utf-8") as file:
            file.write(stl_text)
    return (STL_binary_to_text,)


@app.cell
def __(mo):
    mo.md(rf"""## Constructive Solid Geometry (CSG)

    Have a look at the documentation of [{mo.icon("mdi:github")}fogleman/sdf](https://github.com/fogleman/) and study the basics. At the very least, make sure that you understand what the code below does:
    """)
    return


@app.cell
def __(X, Y, Z, box, cylinder, mo, show, sphere):
    demo_csg = sphere(1) & box(1.5)
    _c = cylinder(0.5)
    demo_csg = demo_csg - (_c.orient(X) | _c.orient(Y) | _c.orient(Z))
    demo_csg.save('output/demo-csg.stl', step=0.05)
    mo.show_code(show("output/demo-csg.stl", theta=45.0, phi=45.0, scale=1.0))
    return (demo_csg,)


@app.cell
def __(mo):
    mo.md("""ℹ️ **Remark.** The same result can be achieved in a more procedural style, with:""")
    return


@app.cell
def __(
    box,
    cylinder,
    difference,
    intersection,
    mo,
    orient,
    show,
    sphere,
    union,
):
    demo_csg_alt = difference(
            intersection(
            sphere(1),
            box(1.5),
        ),
        union(
            orient(cylinder(0.5), [1.0, 0.0, 0.0]),
            orient(cylinder(0.5), [0.0, 1.0, 0.0]),
            orient(cylinder(0.5), [0.0, 0.0, 1.0]),
        ),
    )
    demo_csg_alt.save("output/demo-csg-alt.stl", step=0.05)
    mo.show_code(show("output/demo-csg-alt.stl", theta=45.0, phi=45.0, scale=1.0))
    return (demo_csg_alt,)


@app.cell
def __(mo):
    mo.md(
        rf"""
    ## JupyterCAD

    [JupyterCAD](https://github.com/jupytercad/JupyterCAD) is an extension of the Jupyter lab for 3D geometry modeling.

      - Use it to create a JCAD model that correspond closely to the `output/demo_csg` model;
    save it as `data/demo_jcad.jcad`.

      - Study the format used to represent JupyterCAD files (💡 you can explore the contents of the previous file, but you may need to create some simpler models to begin with).

      - When you are ready, create a `jcad_to_stl` function that understand enough of the JupyterCAD format to convert `"data/demo_jcad.jcad"` into some corresponding STL file.
    (💡 do not tesselate the JupyterCAD model by yourself, instead use the `sdf` library!)


        """
    )
    return


@app.cell
def __(mo):
    mo.md("""## Appendix""")
    return


@app.cell
def __(mo):
    mo.md("""### Dependencies""")
    return


@app.cell
def __():
    # Python Standard Library
    import json

    # Marimo
    import marimo as mo

    # Third-Party Librairies
    import numpy as np
    import matplotlib.pyplot as plt
    import mpl3d
    from mpl3d import glm
    from mpl3d.mesh import Mesh
    from mpl3d.camera import Camera

    import meshio

    np.seterr(over="ignore")  # 🩹 deal with a meshio false warning

    import sdf
    from sdf import sphere, box, cylinder
    from sdf import X, Y, Z
    from sdf import intersection, union, orient, difference

    mo.show_code()
    return (
        Camera,
        Mesh,
        X,
        Y,
        Z,
        box,
        cylinder,
        difference,
        glm,
        intersection,
        json,
        meshio,
        mo,
        mpl3d,
        np,
        orient,
        plt,
        sdf,
        sphere,
        union,
    )


@app.cell
def __(mo):
    mo.md(r"""### STL Viewer""")
    return


@app.cell
def __(Camera, Mesh, glm, meshio, mo, plt):
    def show(
        filename,
        theta=0.0,
        phi=0.0,
        scale=1.0,
        colormap="viridis",
        edgecolors=(0, 0, 0, 0.25),
        figsize=(6, 6),
    ):
        fig = plt.figure(figsize=figsize)
        ax = fig.add_axes([0, 0, 1, 1], xlim=[-1, +1], ylim=[-1, +1], aspect=1)
        ax.axis("off")
        camera = Camera("ortho", theta=theta, phi=phi, scale=scale)
        mesh = meshio.read(filename)
        vertices = glm.fit_unit_cube(mesh.points)
        faces = mesh.cells[0].data
        vertices = glm.fit_unit_cube(vertices)
        mesh = Mesh(
            ax,
            camera.transform,
            vertices,
            faces,
            cmap=plt.get_cmap(colormap),
            edgecolors=edgecolors,
        )
        return mo.center(fig)

    mo.show_code()
    return (show,)


@app.cell
def __(mo, show):
    mo.show_code(show("data/teapot.stl", theta=45.0, phi=30.0, scale=2))
    return


if __name__ == "__main__":
    app.run()
