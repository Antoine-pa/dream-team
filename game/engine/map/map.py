import pygame
from engine import cst, t

class Map:
    def __init__(self):
        self.x = 1000 #nombre de case
        self.y = 1000
        self.pos = [self.x/2, self.y/2] #position actuelle de l'affichage dans la map
        self.list_build = {0:[], -1:[]} #liste des batiments construits
        self.dict_name_build = {0:{}, -1:{}}
        self.dict_kind_build = {0:{}, -1:{}}
        self.dict_pos_build = {0:{}, -1:{}}
        self.layer = 0

    def __repr__(self):
        return f"Map :\n - taille : {self.x}x{self.y}\n - position : {self.pos}\n - bâtiments : {self.list_build}"

    def display(self, screen):
        """
        affichage de la map
        """
        if self.layer == 0:
            color1 = cst("WHITE")
            color2 = cst("BLACK")
        else:
            color1 = cst("BLACK")
            color2 = cst("WHITE")

        screen.fill(color1)
        for x in range(0, cst("size_x")+int(cst("SIZE_CASE")), int(cst("SIZE_CASE"))):
            pygame.draw.line(screen, color2, (x-self.pos[0]%1*int(cst("SIZE_CASE")), 0), (x-self.pos[0]%1*int(cst("SIZE_CASE")), cst("size_y")))
            for y in range(0, cst("size_y")+int(cst("SIZE_CASE")), int(cst("SIZE_CASE"))):
                pygame.draw.line(screen, color2, (0, y-self.pos[1]%1*int(cst("SIZE_CASE"))), (cst("size_x"), y-self.pos[1]%1*int(cst("SIZE_CASE"))))
        for y in range(int(self.pos[1])-10, int(self.pos[1]+cst("size_y")//cst("SIZE_CASE"))+2):
            for x in range(int(self.pos[0])-10, int(self.pos[0]+cst("size_x")//cst("SIZE_CASE"))+2):
                b = self.dict_pos_build[self.layer].get((x, y))
                if b is not None:
                    d = b.display(screen, *self.pos)
        for b in self.dict_kind_build[self.layer].get("production", []):
            if b.start_production:
                if t.check_product(b):
                    color = cst("GREEN")
                else:
                    color = cst("RED")
                pygame.draw.rect(screen, color, pygame.Rect((b.pos[0]-self.pos[0])*int(cst("SIZE_CASE"))+cst("SIZE_CASE")//6, (b.pos[1]-self.pos[1])*int(cst("SIZE_CASE"))+cst("SIZE_CASE")//6, cst("SIZE_CASE")//6, cst("SIZE_CASE")//6), 0)
                
    def add_build(self, build):
        """
        ajout d'un bâtiment dans la liste des batiments et dans les cases occupées
        """
        self.list_build[self.layer].append(build)

        for x in range(build.pos[0], build.pos[0]+build.size[0]):
            for y in range(build.pos[1], build.pos[1]+build.size[1]):
                self.dict_pos_build[self.layer][(x, y)] = build

        if self.dict_name_build[self.layer].get(build.name) is None:
            self.dict_name_build[self.layer][build.name] = []
        self.dict_name_build[self.layer][build.name].append(build)

        if self.dict_kind_build[self.layer].get(build.kind) is None:
            self.dict_kind_build[self.layer][build.kind] = []
        self.dict_kind_build[self.layer][build.kind].append(build)

        if build.kind == "production":
            build.start_production = True
        if build.name == "Wall":
            build.load()

    def sup_build(self, build):
        self.list_build[self.layer].remove(build)
        self.dict_kind_build[self.layer][build.kind].remove(build)
        self.dict_name_build[self.layer][build.name].remove(build)
        for x in range(build.pos[0], build.pos[0]+build.size[0]):
            for y in range(build.pos[1], build.pos[1]+build.size[1]):
                del self.dict_pos_build[self.layer][(x, y)]
    
    def check_pos(self, build, cases_mem_tamp) -> int: #0 = libre, 1 = un batiment construit donc pas libre, 2 = un batiment posé, en memoire tampon donc pas libre
        """
        vérifie que la case est libre pour le bâtiment build
        """
        if tuple(build.pos) in cases_mem_tamp:
            return 2
        for x in range(build.pos[0], build.pos[0]+build.size[0]):
            for y in range(build.pos[1], build.pos[1]+build.size[1]):
                if (x, y) in list(self.dict_pos_build[self.layer].keys())+cases_mem_tamp:
                    return 1
        return 0
    
    def reload_images(self):
        """
        recharge les images (après un zoom)
        """
        for c in self.list_build.items():
            for b in c[1]:
                b.load()
    
    def zoom(self, z):
        if z < 0 and cst("ZOOM") >= 1.1 or z > 0 and cst("ZOOM") <= 1.9:
            old_zoom = cst("ZOOM")
            t.set_const("ZOOM", round(cst("ZOOM") + z/10, 1))
            t.set_const("SIZE_CASE", 1/cst("ZOOM")*cst("SIZE_CASE")/(1/old_zoom))
            return True
        return False