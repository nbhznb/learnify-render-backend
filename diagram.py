import json
import argparse
import logging
import os
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def setup_2d_figure(figsize=(8, 8)):
    """Create and configure a 2D matplotlib figure and axis."""
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis('off')
    return fig, ax


def setup_3d_figure(figsize=(10, 8)):
    """Create and configure a 3D matplotlib figure and axis."""
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection='3d')
    ax.grid(False)
    ax.set_axis_off()
    return fig, ax


def draw_regular_polygon(ax, center: tuple, radius: float, num_sides: int, **kwargs) -> np.ndarray:
    """
    Draw a regular polygon on a given 2D axis.
    Returns the computed vertices as an (N,2) array.
    """
    angles = np.linspace(0, 2 * np.pi, num_sides, endpoint=False)
    vertices = np.column_stack((center[0] + radius * np.cos(angles),
                                center[1] + radius * np.sin(angles)))
    polygon = plt.Polygon(vertices, **kwargs)
    ax.add_patch(polygon)
    return vertices


def draw_3d_shape(ax, vertices: np.ndarray, faces: list, color='lightgray'):
    """
    Helper function to draw 3D shapes using Poly3DCollection.
    """
    collection = Poly3DCollection(
        [vertices[face] for face in faces],
        facecolors=color,
        edgecolors='black',
        alpha=0.6
    )
    ax.add_collection3d(collection)


def add_description(fig, shape):
    """
    Add a text description to the figure with shape information and the question text.
    """
    shape_info = shape.get("shape", {})
    question_text = shape.get("text", "")
    # Build details string from shape_info (excluding the "type" key)
    details = ", ".join(
        [f"{k.replace('_', ' ').capitalize()} = {v}" for k, v in shape_info.items() if k != "type"]
    )
    shape_type = shape_info.get("type", "").replace('_', ' ').capitalize()
    description = f"{shape_type} ({details})\n{question_text}"
    # Place the text at the bottom-center of the figure
    fig.text(0.5, 0.02, description, ha="center", va="bottom", fontsize=12)


def draw_shape(shape_data: list, shape_id: int = None, output_folder="static/result"):
    """
    Draws shape(s) from the provided data and saves the resulting image(s) into output_folder.
    """
    if shape_id is not None:
        shape_data = [shape for shape in shape_data if shape["id"] == shape_id]
        if not shape_data:
            logging.error(f"No shape found with ID {shape_id}.")
            return

    # Ensure output folder exists - make it relative to current working directory
    if not os.path.isabs(output_folder):
        output_folder = os.path.join(os.getcwd(), output_folder)
    
    os.makedirs(output_folder, exist_ok=True)

    # Also ensure other needed directories exist
    tmp_dir = os.path.join(os.getcwd(), "static", "tmp")
    os.makedirs(tmp_dir, exist_ok=True)

    for shape in shape_data:
        current_id = shape["id"]
        shape_info = shape.get("shape")
        if not shape_info:
            logging.warning(f"Skipping shape with ID {current_id} as it has no shape property.")
            continue

        shape_type = shape_info["type"]
        fig = None

        # 2D Regular Polygons
        if shape_type in [
            "triangle", "square", "pentagon", "hexagon", "heptagon",
            "octagon", "nonagon", "decagon", "dodecagon"
        ]:
            fig, ax = setup_2d_figure(figsize=(8, 8))
            side_length = shape_info.get("side", 10)
            num_sides = {
                "triangle": 3, "square": 4, "pentagon": 5,
                "hexagon": 6, "heptagon": 7, "octagon": 8,
                "nonagon": 9, "decagon": 10, "dodecagon": 12
            }[shape_type]
            radius = side_length / (2 * np.sin(np.pi / num_sides))
            center = (radius + 1, radius + 1)
            # Draw the polygon (no extra side labels)
            _ = draw_regular_polygon(ax, center, radius, num_sides, fill=False, edgecolor='black')
            margin = radius * 0.2
            ax.set_xlim(0, 2 * (radius + margin))
            ax.set_ylim(0, 2 * (radius + margin))

        # Special 2D Shapes
        elif shape_type in ["rectangle", "parallelogram", "trapezoid", "rhombus", "kite"]:
            fig, ax = setup_2d_figure(figsize=(8, 8))
            if shape_type == "rectangle":
                # Support both "length" & "width" (preferred) or "width" & "height"
                if "length" in shape_info and "width" in shape_info:
                    rect_length = shape_info["length"]
                    rect_height = shape_info["width"]
                else:
                    rect_length = shape_info.get("width", 10)
                    rect_height = shape_info.get("height", 6)
                rect = plt.Rectangle((1, 1), rect_length, rect_height, fill=False, edgecolor='black')
                ax.add_patch(rect)
                ax.text(1 + rect_length / 2, 1 - 0.5, f"Length = {rect_length} cm", ha='center')
                ax.text(1 - 0.5, 1 + rect_height / 2, f"Width = {rect_height} cm", va='center', rotation=90)
                ax.set_xlim(0, rect_length + 2)
                ax.set_ylim(0, rect_height + 2)
            elif shape_type == "parallelogram":
                base = shape_info.get("base", 8)
                height = shape_info.get("height", 6)
                shear = 0.5  # adjust this to control the slant
                vertices = np.array([
                    (1, 1),
                    (1 + base, 1),
                    (1 + base + shear * height, 1 + height),
                    (1 + shear * height, 1 + height)
                ])
                ax.add_patch(plt.Polygon(vertices, fill=False, edgecolor='black'))
                ax.set_xlim(0, vertices[:, 0].max() + 1)
                ax.set_ylim(0, vertices[:, 1].max() + 1)
            elif shape_type == "trapezoid":
                width_val = shape_info.get("width", 10)
                height_val = shape_info.get("height", 6)
                top_width = shape_info.get("top_width", width_val * 0.6)
                offset = (width_val - top_width) / 2
                vertices = np.array([
                    (1, 1),
                    (1 + width_val, 1),
                    (1 + width_val - offset, 1 + height_val),
                    (1 + offset, 1 + height_val)
                ])
                ax.add_patch(plt.Polygon(vertices, fill=False, edgecolor='black'))
                ax.set_xlim(0, width_val + 2)
                ax.set_ylim(0, height_val + 2)

            elif shape_type in ["rhombus", "kite"]:
                if shape_type == "rhombus":
                    width_val = shape_info.get("width", 10)
                    height_val = shape_info.get("height", 6)
                    vertices = np.array([
                        (1, 1 + height_val / 2),
                        (1 + width_val / 2, 1),
                        (1 + width_val, 1 + height_val / 2),
                        (1 + width_val / 2, 1 + height_val)
                    ])
                else:  # kite
                    diagonals = shape_info.get("diagonals", [14, 10])
                    d1, d2 = diagonals  # first and second diagonal
                    vertices = np.array([
                        (1, 1 + d2/2),           # left vertex
                        (1 + d1 * 0.75, 1),       # top vertex (offset from center)
                        (1 + d1, 1 + d2/2),       # right vertex
                        (1 + d1 * 0.75, 1 + d2)   # bottom vertex (offset from center)
                    ])

                ax.add_patch(plt.Polygon(vertices, fill=False, edgecolor='black'))
                ax.set_xlim(0, vertices[:, 0].max() + 1)
                ax.set_ylim(0, vertices[:, 1].max() + 1)


        # Triangle Types (Isosceles, Scalene, Equilateral)
        elif shape_type in ["isosceles_triangle", "scalene_triangle", "equilateral_triangle"]:
            fig, ax = setup_2d_figure(figsize=(8, 8))
            base = shape_info.get("base", 10)
            height_val = shape_info.get("height", 8)
            if shape_type == "equilateral_triangle":
                side = base
                height_val = side * np.sqrt(3) / 2
                vertices = np.array([
                    (1, 1),
                    (1 + side, 1),
                    (1 + side / 2, 1 + height_val)
                ])
            elif shape_type == "isosceles_triangle":
                vertices = np.array([
                    (1, 1),
                    (1 + base, 1),
                    (1 + base / 2, 1 + height_val)
                ])
            else:  # scalene_triangle
                vertices = np.array([
                    (1, 1),
                    (1 + base, 1),
                    (1 + base / 3, 1 + height_val)
                ])
            ax.add_patch(plt.Polygon(vertices, fill=False, edgecolor='black'))
            ax.set_xlim(0, base + 2)
            ax.set_ylim(0, height_val + 2)

        # 3D Shapes
        elif shape_type in [
            "cube", "cuboid", "rectangular_prism", "cone", "sphere", "hemisphere",
            "rectangular_pyramid", "hexagonal_prism", "pentagonal_prism",
            "triangular_prism", "square_pyramid"
        ]:
            fig, ax = setup_3d_figure(figsize=(10, 8))
            if shape_type == "triangular_prism":
                base_area = shape_info.get("base_area", 35)
                height_val = shape_info.get("height", 20)
                side = np.sqrt(4 * base_area / np.sqrt(3))
                vertices = np.array([
                    [0, 0, 0],
                    [side, 0, 0],
                    [side / 2, side * np.sqrt(3) / 2, 0],
                    [0, 0, height_val],
                    [side, 0, height_val],
                    [side / 2, side * np.sqrt(3) / 2, height_val]
                ])
                faces = [
                    [0, 1, 2],      # bottom triangle
                    [3, 4, 5],      # top triangle
                    [0, 1, 4, 3],   # front face
                    [1, 2, 5, 4],   # right face
                    [2, 0, 3, 5]    # left face
                ]
                draw_3d_shape(ax, vertices, faces)
            elif shape_type == "square_pyramid":
                base_area = shape_info.get("base_area", 40)
                height_val = shape_info.get("height", 25)
                side = np.sqrt(base_area)
                vertices = np.array([
                    [0, 0, 0],
                    [side, 0, 0],
                    [side, side, 0],
                    [0, side, 0],
                    [side / 2, side / 2, height_val]
                ])
                faces = [
                    [0, 1, 2, 3],  # base
                    [0, 1, 4],     # front face
                    [1, 2, 4],     # right face
                    [2, 3, 4],     # back face
                    [3, 0, 4]      # left face
                ]
                draw_3d_shape(ax, vertices, faces)
            elif shape_type == "cube":
                side = shape_info.get("side", 10)
                vertices = np.array([
                    [0, 0, 0], [side, 0, 0], [side, side, 0], [0, side, 0],
                    [0, 0, side], [side, 0, side], [side, side, side], [0, side, side]
                ])
                faces = [
                    [0, 1, 2, 3], [4, 5, 6, 7],
                    [0, 1, 5, 4], [1, 2, 6, 5],
                    [2, 3, 7, 6], [3, 0, 4, 7]
                ]
                draw_3d_shape(ax, vertices, faces)
            elif shape_type in ["cuboid", "rectangular_prism"]:
                length = shape_info.get("length", 10)
                width_val = shape_info.get("width", 6)
                height_val = shape_info.get("height", 8)
                vertices = np.array([
                    [0, 0, 0],
                    [length, 0, 0],
                    [length, width_val, 0],
                    [0, width_val, 0],
                    [0, 0, height_val],
                    [length, 0, height_val],
                    [length, width_val, height_val],
                    [0, width_val, height_val]
                ])
                faces = [
                    [0, 1, 2, 3],
                    [4, 5, 6, 7],
                    [0, 1, 5, 4],
                    [1, 2, 6, 5],
                    [2, 3, 7, 6],
                    [3, 0, 4, 7]
                ]
                draw_3d_shape(ax, vertices, faces)
            elif shape_type in ["cone", "sphere", "hemisphere"]:
                radius_val = shape_info.get("radius", 5)
                height_val = shape_info.get("height", 10) if shape_type == "cone" else radius_val
                if shape_type == "cone":
                    theta = np.linspace(0, 2 * np.pi, 100)
                    z = np.linspace(0, height_val, 100)
                    theta, z = np.meshgrid(theta, z)
                    r = radius_val * (1 - z / height_val)
                    x = r * np.cos(theta)
                    y = r * np.sin(theta)
                    ax.plot_surface(x, y, z, color='lightgray', alpha=0.6)
                else:
                    phi = np.linspace(0, np.pi if shape_type == "sphere" else np.pi / 2, 100)
                    theta = np.linspace(0, 2 * np.pi, 100)
                    phi, theta = np.meshgrid(phi, theta)
                    x = radius_val * np.sin(phi) * np.cos(theta)
                    y = radius_val * np.sin(phi) * np.sin(theta)
                    z = radius_val * np.cos(phi)
                    ax.plot_surface(x, y, z, color='lightgray', alpha=0.6)
            elif shape_type in ["hexagonal_prism", "pentagonal_prism"]:
                side = shape_info.get("side", 5)
                height_val = shape_info.get("height", 15)
                n_sides = 6 if shape_type == "hexagonal_prism" else 5
                angles = np.linspace(0, 2 * np.pi, n_sides, endpoint=False)
                base_vertices = np.column_stack((side * np.cos(angles), side * np.sin(angles)))
                bottom = np.hstack([base_vertices, np.zeros((n_sides, 1))])
                top = np.hstack([base_vertices, np.full((n_sides, 1), height_val)])
                vertices = np.vstack([bottom, top])
                faces = [list(range(n_sides)), list(range(n_sides, 2 * n_sides))]
                for i in range(n_sides):
                    faces.append([i, (i + 1) % n_sides, n_sides + ((i + 1) % n_sides), n_sides + i])
                draw_3d_shape(ax, vertices, faces)
            ax.set_box_aspect([1, 1, 1])
        else:
            logging.warning(f"Shape type {shape_type} not implemented yet.")
            continue

        # Add the text description to every generated image.
        add_description(fig, shape)

        if fig:
            filepath = os.path.join(output_folder, f"{current_id}.png")
            plt.savefig(filepath, bbox_inches="tight", dpi=300)
            plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description="Generate shape images from JSON data.")
    parser.add_argument("--id", type=int, help="Specific shape ID to generate")
    parser.add_argument("--file", type=str, default="test.json", help="Path to the JSON file containing shapes")
    args = parser.parse_args()

    try:
        with open(args.file, "r") as file:
            shapes = json.load(file)
    except Exception as e:
        logging.error(f"Error reading file {args.file}: {e}")
        return

    draw_shape(shapes, shape_id=args.id)
    logging.info("Images generated successfully!")


if __name__ == "__main__":
    main()
