import copy as c
import math
import random

from PIL import Image, ImageDraw

generations = 1000000
example = Image.open('Malysh.png')

example = example.convert('RGBA')
width, height = example.size

colors = example.getcolors(width*height)


def create_genome():
    circles = []

    center = (random.randint(200, 300), random.randint(0, height))
    radius = 7
    number = random.randint(0, len(colors) - 1)
    frequency, color = colors[number]
    alpha = 200

    circles.append([center, radius, color[0], color[1], color[2], alpha])

    return circles


def render_descendant(genome):
    out = Image.new("RGBA", (width, height), "white")
    base = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(base)

    for item in genome:
        x, y = item[0]
        radius = item[1]
        r = item[2]
        g = item[3]
        b = item[4]
        a = item[5]

        color = (r, g, b, a)

        draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=color)
        out = Image.alpha_composite(out, base)

    return out


def mutate(origin):
    copy = c.copy(origin)

    center = (random.randint(0, width), random.randint(0, height))
    radius = 7
    number = random.randint(0, len(colors) - 1)
    frequency, color = colors[number]
    alpha = 200

    copy.append([center, radius, color[0], color[1], color[2], alpha])

    return copy, center, radius


def fitness(original, new, center, radius):
    fitnes = 0
    x, y = center
    if x - 2 * radius > 0:
        x0 = x - 2 * radius
    else:
        x0 = 0

    if x + 2 * radius < width - 1:
        x1 = x + 2 * radius
    else:
        x1 = width

    if y - 2 * radius > 0:
        y0 = y - 2 * radius
    else:
        y0 = 0

    if y + 2 * radius < width - 1:
        y1 = y + 2 * radius
    else:
        y1 = width

    for x in range(x0, x1):
        for y in range(y0, y1):
            r1, g1, b1, a1 = original.getpixel((x, y))
            r2, g2, b2, a2 = new.getpixel((x, y))

            delta_red = (r1 - r2) ** 2
            delta_green = (g1 - g2) ** 2
            delta_blue = (b1 - b2) ** 2
            delta_alpha = (a1 - a2) ** 2

            pixel_fitness = math.sqrt(delta_red + delta_green + delta_blue + delta_alpha)

            fitnes += pixel_fitness

    return fitnes


def generate():
    best_genome = create_genome()

    for i in range(generations):
        daughter = c.copy(best_genome)
        daughter, center, radius = mutate(daughter)

        fitness_daughter = fitness(example, render_descendant(daughter), center, radius)

        if fitness_daughter < fitness(example, render_descendant(best_genome), center, radius):
            best_genome = daughter

        if i % 50 == 0:
            print(i)
        if i % 1000 == 0:
            render_descendant(best_genome).save("result" + str(i) + ".png", dpi=(512, 512))


generate()
