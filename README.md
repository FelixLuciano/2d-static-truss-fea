[Caio Santos, Dr](http://lattes.cnpq.br/8164040695755574). Transferências de Calor e Mecânica dos Sólidos. [Insper](https://github.com/Insper), 2022.

# 2D Static Truss Finite Element Analysis


## Introduction

A [finite element analysis](https://en.wikipedia.org/wiki/Finite_element_method) (FEA) software is a computer program that uses the finite element method (FEM) to analyze and solve problems in engineering and science. The finite element method is a numerical technique for solving differential equations that describe physical phenomena, such as the behavior of structures under load or the flow of fluids through pipes.

Finite element analysis software is used in a wide range of engineering and scientific applications, including structural analysis, fluid dynamics, heat transfer, and electromagnetics. It can be used to analyze the performance of structures under different loads, predict the behavior of materials under various conditions, and optimize designs for improved performance.

Some common features of finite element analysis software include the ability to:
- Model complex geometries and boundary conditions
- Solve for static, dynamic, and thermal behaviors
- Analyze nonlinear behavior, such as material plasticity or contact
- Import and export data from other software programs
- Generate detailed reports and visualizations of results

There are many different finite element analysis software packages available on the market, ranging from simple programs with a limited range of capabilities to more advanced packages with a wide range of features and functionality.

### Gauss-Seidel method

The [Gauss-Seidel method](https://en.wikipedia.org/wiki/Gauss%E2%80%93Seidel_method) is an iterative method for solving systems of linear equations, which can be used in the context of finite element analysis (FEA) to solve for unknown nodal displacements in a finite element model. It is a type of relaxation method that is used to find approximate solutions to systems of equations by iteratively improving upon an initial guess.


### Beam Element

In structural engineering, a [beam element](https://en.wikipedia.org/wiki/Beam_(structure)) is a structural element that is capable of withstanding load primarily by resisting bending. Beam elements are usually straight and slender, and they are often used to construct the vertical supports of a structure, such as columns, and the horizontal members that transfer loads from the vertical supports to the foundation, such as beams and girders.

Beam elements can be made of various materials, including concrete, steel, timber, and composite materials. They are typically designed to resist loads that are applied along their length, such as gravity loads, wind loads, and earthquake loads. The strength and stiffness of beam elements are typically determined by the size, shape, and material properties of the element.

In structural analysis and design, beam elements are often modeled using mathematical equations that describe the behavior of the element under various load conditions. These equations can be used to predict the deflections, stresses, and strains in the beam element, and to design the element to meet the required strength and stiffness criteria.

![Beam element displacement](assets/image/beam-element.png)

$$
\begin{Bmatrix} 
    \bar u_1 \\
    \bar u_2 \\
\end{Bmatrix}
=
\underbrace{
    \begin{bmatrix} 
        \cos(\theta) & \sin(\theta) & 0 & 0 \\
        0 & 0 & \cos(\theta) & \sin(\theta)\\
    \end{bmatrix}
}_T
\cdot
\begin{Bmatrix} 
    u_1 \\
    v_1 \\
    u_2 \\
    v_2 \\
\end{Bmatrix}
$$

$$
x=\bar u_2-\bar u_1=
\begin{bmatrix} 
    -\cos(\theta) & -\sin(\theta) & \cos(\theta) & \sin(\theta) \\
\end{bmatrix}
\cdot
\begin{Bmatrix} 
    u_1 \\
    v_1 \\
    u_2 \\
    v_2 \\
\end{Bmatrix}
$$

$$
\begin{Bmatrix} 
    \bar F_1 \\
    \bar F_2 \\
\end{Bmatrix}
=
\underbrace{
    \frac{EA}{l}
    \begin{bmatrix} 
        1 & -1 \\
        -1 & 1 \\
    \end{bmatrix}
}_{\bar K_e}
\cdot
\begin{Bmatrix} 
    \bar u_1 \\
    \bar u_2 \\
\end{Bmatrix}
$$

$$
\begin{Bmatrix} 
    F_1 \\
    F_2 \\
\end{Bmatrix}
=
\underbrace{
    T^T\cdot\bar K_e\cdot T
}_{K_e}
\cdot
\begin{Bmatrix} 
    u_1 \\
    v_1 \\
    u_2 \\
    v_2 \\
\end{Bmatrix}
$$

$$
\bar F=K_e\cdot x
$$

## Instalation
```
pip install https://github.com/FelixLuciano/2d-static-truss-fea/archive/refs/heads/master.tar.gz
```


## Examples

### Shelf

![Shelf example](examples/shelf/output.png)

[View source](examples/shelf/source.py)

### Pyramid

![Pyramid example](examples/pyramid/output.png)

[View source](examples/pyramid/source.py)

### Bridge

![Bridge example](examples/bridge/output.gif)

[View source](examples/bridge/source.py)


## Authors

<table width="100%">
    <tr>
        <td align="center">
            <a href="https://github.com/DiogoDuarteInsper"><img src="https://avatars.githubusercontent.com/u/62605906?v=4" style="width: 50%;" /></a>
        </td>
        <td align="center">
            <a href="https://github.com/JorasOliveira"><img src="https://avatars.githubusercontent.com/u/43121361?v=4" style="width: 50%;" /><br /></a>
        </td>
        <td align="center">
            <a href="https://github.com/FelixLuciano"><img src="https://avatars.githubusercontent.com/u/22255332?v=4" style="width: 50%;" /><br /></a>
        </td>
    </tr>
    <tr>
        <td align="center">
            <a href="https://github.com/DiogoDuarteInsper"><strong>Diogo Duarte</strong></a>
        </td>
        <td align="center">
            <a href="https://github.com/JorasOliveira"><strong>Joras Oliveira</strong></a>
        </td>
        <td align="center">
            <a href="https://github.com/FelixLuciano"><strong>Luciano Felix</strong></a>
        </td>
    </tr>
</table>


## Competition

### Photos
<details>
<summary>Expand</summary>
<img src="assets/image/20221103_193053.jpg" alt="Photo">
<img src="assets/image/20221103_193049.jpg" alt="Photo">
</details>

## License
This project is [MIT licensed](LICENSE)!
