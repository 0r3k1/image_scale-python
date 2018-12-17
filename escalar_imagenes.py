#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame, os
from pygame.locals import *
from pygame.color import *

formatos = ("BMP", "TGA", "PNG", "JPEG", "bmp", "tga", "png", "jpeg")

def ls(ruta=os.getcwd()):
    lista = [archivo.name for archivo in os.scandir(ruta) if archivo.is_file()]
    lista.sort()
    return lista

def lista_imagenes(lista):
    img = []
    for i in lista:
        img.append(pygame.image.load(i).convert_alpha())
    return img

def imagens_fondo(lista):
    l = []
    for i in lista:
        ext = i.split(".")
        if ext[len(ext)-1] == "png":
            l.append("img{0}{1}".format(os.sep, i))

    return lista_imagenes(l)

def menu_inicio(ventana, fondo):
    clock = pygame.time.Clock()

    mouse = pygame.Rect((0,0), (10,15))
    estado = 0

    rect1 = pygame.Rect(43, 148, 314, 178)
    rect2 = pygame.Rect(400, 148, 287, 178)

    quit = False

    while not quit:
        for event in pygame.event.get():
            if event.type == QUIT: quit = True
            if event.type == MOUSEMOTION:
                mouse.topleft = pygame.mouse.get_pos()
                if rect1.colliderect(mouse):
                    estado = 1
                elif rect2.colliderect(mouse):
                    estado = 2
                else: estado = 0
            if event.type == MOUSEBUTTONDOWN:
                if estado == 1 or estado == 2:
                    return estado

        ventana.blit(fondo[estado], (0,0))
        pygame.display.update()
        clock.tick(30)

    pygame.quit()
    os._exit(1)

def escrive(event, txt):
    abc = ("a", "b", "c", "d", "e" , "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z")
    num = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

    if event.key == K_ESCAPE:
        return "{0} ".format(txt)
    if event.key == K_BACKSPACE:
        return txt[:-1]
    if event.key >= K_a and event.key <= K_z:
        return "{0}{1}".format(txt, abc[event.key-K_a])
    if event.key >= K_0 and event.key <= K_9:
        return "{0}{1}".format(txt, num[event.key-K_0])
    if event.key >= K_KP0 and event.key <= K_KP9:
        return "{0}{1}".format(txt, num[event.key-K_KP0])

def datos_escala(ventana, fondo):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 50)

    mouse = pygame.Rect((0,0), (10,15))
    quit = False
    ok = False
    carpeta = ""
    ancho = ""
    alto = ""

    focus = 0

    rect_ruta = pygame.Rect(170, 82, 383, 65)
    rect_ancho = pygame.Rect(110, 256, 236, 65)
    rect_alto = pygame.Rect(395, 256, 236, 65)

    btn_atras = pygame.Rect(395, 388, 94, 64)
    btn_ok = pygame.Rect(569, 388, 94, 64)

    while not quit and not ok:
        for event in pygame.event.get():
            if event.type == QUIT: quit = True
            if event.type == KEYDOWN:
                if (focus == 1 and len(carpeta) < 15) or (focus == 1 and event.key == K_BACKSPACE):
                    carpeta = escrive(event, carpeta)
                elif (focus == 2 and len(ancho) < 4) or (focus == 2 and event.key == K_BACKSPACE):
                    ancho = escrive(event, ancho)
                elif (focus == 3 and len(alto) < 4) or (focus == 3 and event.key == K_BACKSPACE):
                    alto = escrive(event, alto)
            if event.type == MOUSEMOTION:
                mouse.topleft = pygame.mouse.get_pos()
            if event.type == MOUSEBUTTONDOWN:
                if rect_ruta.colliderect(mouse):
                    focus = 1
                elif rect_ancho.colliderect(mouse):
                    focus = 2
                elif rect_alto.colliderect(mouse):
                    focus = 3
                else: focus = 0

                if btn_atras.colliderect(mouse):
                    return "atras"
                elif btn_ok.colliderect(mouse):
                    ok = True

        surf_carpeta = font.render(carpeta, 1, THECOLORS["white"])
        surf_ancho = font.render(ancho, 1, THECOLORS["white"])
        surf_alto = font.render(alto, 1, THECOLORS["white"])

        ventana.blit(fondo, (0,0))
        ventana.blit(surf_carpeta, rect_ruta.topleft)
        ventana.blit(surf_ancho, rect_ancho.topleft)
        ventana.blit(surf_alto, rect_alto.topleft)
        pygame.display.update()
        clock.tick(30)

    if quit:
        pygame.quit()
        os._exit(1)

    if carpeta == "": return None
    try:
        int(ancho)
        int(alto)
    except ValueError:
        return None

    return (carpeta, ancho, alto)

def datos_tiled(ventana, fondo):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 30)

    path = "{0}{1}{2}".format(os.getcwd(), os.sep, "tile_sheet")
    if not os.path.exists(path):
        os.mkdir(path)

    tiles = ls(path)
    for i in tiles:
        name = i.split(".")
        if not name[len(name)-1] in formatos:
            tiles.remove(i)

    dta = []
    txt = []
    cola = 0
    focus = 0
    ancho = ""
    alto = ""

    btn_atras = pygame.Rect(395, 388, 94, 64)
    btn_ok = pygame.Rect(569, 388, 94, 64)
    rect_ancho = pygame.Rect(100, 189, 238, 68)
    rect_alto = pygame.Rect(386, 189, 238, 68)
    mouse = pygame.Rect((0,0), (10,15))

    for i in range(len(tiles)):
        txt.append(font.render(tiles[i], 1, THECOLORS["white"]))

    mouse = pygame.Rect((0,0), (10,15))
    quit = False

    while not quit:
        for event in pygame.event.get():
            if event.type == QUIT: quit = True
            if event.type == KEYDOWN:
                if (focus == 1 and len(ancho) < 4) or (focus == 1 and event.key == K_BACKSPACE):
                    ancho = escrive(event, ancho)
                elif (focus == 2 and len(alto) < 4) or (focus == 2 and event.key == K_BACKSPACE):
                    alto = escrive(event, alto)
            if event.type == MOUSEMOTION:
                mouse.topleft = pygame.mouse.get_pos()
            if event.type == MOUSEBUTTONDOWN:
                if rect_ancho.colliderect(mouse):
                    focus = 1
                elif rect_alto.colliderect(mouse):
                    focus = 2
                else: focus = 0

                if btn_ok.colliderect(mouse):
                    if ancho.isdigit() and alto.isdigit():
                        dta.append([tiles[cola], int(ancho), int(alto)])
                        ancho = ""
                        alto = ""
                        cola += 1
                elif btn_atras.colliderect(mouse):
                    cola -= 1


        if cola < 0:
            return "atras"
        elif cola >= len(txt):
            return dta

        pos = (ventana.get_width()/2) - (txt[cola].get_width()/2)
        surf_ancho = font.render(ancho, 1, THECOLORS["white"])
        surf_alto = font.render(alto, 1, THECOLORS["white"])

        ventana.blit(fondo[0], (0,0))
        ventana.blit(txt[cola], (pos, 30))
        ventana.blit(surf_ancho, rect_ancho.topleft)
        ventana.blit(surf_alto, rect_alto.topleft)
        pygame.display.update()
        clock.tick(30)

    if quit:
        pygame.quit()
        os._exit(1)


def cut_tiled(dta):
    for item in dta:
        name = item[0].split(".")
        carpeta = "tile_sheet{0}{1}".format(os.sep, name[0])
        if not os.path.exists(carpeta):
            os.mkdir(carpeta)

        img = pygame.image.load("tile_sheet{0}{1}".format(os.sep, item[0])).convert_alpha()

        x_tam = int(img.get_width()/item[1])
        y_tam = int(img.get_height()/item[2])

        for j in range(y_tam):
            for i in range(x_tam):
                img.set_clip(pygame.Rect(i*item[1], j*item[2], item[1], item[2]))
                sub = img.subsurface(img.get_clip())
                pygame.image.save(sub, "{0}{1}{2}_{3:0>4}.{4}".format(carpeta, os.sep, name[0], j*y_tam+i, name[len(name)-1]))


def escala(dta):
    ruta = ls("{0}{1}{2}".format(os.getcwd(), os.sep, dta[0]))
    path = "{0}{1}{2}".format(os.getcwd(), os.sep, "{0}_{1}x{2}px".format(dta[0],dta[1],dta[2]))
    if os.path.exists(path):
        rm = ls(path)
        for i in rm:
            os.remove(i)
        os.rmdir(path)

    os.mkdir(path)

    for i in ruta:
        name = i.split(".")
        if not name[len(name)-1] in formatos:
            ruta.remove(i)

    for i in ruta:
        img = pygame.image.load("{0}{1}{2}".format(dta[0], os.sep, i))
        img = pygame.transform.scale(img, (int(dta[1]), int(dta[2])))
        pygame.image.save(img, "{0}{1}{2}".format(path, os.sep, i))


def main():
    pygame.init()
    ventana = pygame.display.set_mode((720,480))
    pygame.display.set_caption("escalar")

    fondo = imagens_fondo(ls("{0}{1}img".format(os.getcwd(), os.sep)))
    repeat = True
    tiled = 1
    esc = 2

    while repeat:
        op = menu_inicio(ventana, fondo)
        if op == tiled:
            dta = datos_tiled(ventana, fondo[4:])
        elif op == esc:
            dta = datos_escala(ventana, fondo[3])

        if dta == "atras":
            repeat = True
        elif dta == None:
            print("error: 405")
        else:
            repeat = False

    if op == tiled:
        cut_tiled(dta)
    elif op == esc:
        escala(dta)

    pygame.quit()



if __name__ == '__main__':
    main()
