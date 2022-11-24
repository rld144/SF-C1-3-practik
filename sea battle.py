from random import randint

class SBException(Exception):
    def __str__(self):
        return 'BAD CODE'
class PolygonOutException(SBException):
    def __str__(self):
        return 'выстрел за полигон'
class PolygonRepeatedShot(SBException):
    def __str__(self):
        return 'тут вы уже стреляли'

class Dot:
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.x

    def __repr__(self):
        return f"({self.x}, {self.y})"

class Ship(Dot):
    def __init__(self, x, y, length=1, x_end=None, y_end=None): #тут точки носа и хвоста корабля, в начале думал так удобнее
        if x == x_end or y == y_end:
            super().__init__(x, y)
            self.length = length
            self.x_end = x_end
            self.y_end = y_end
        else:
            raise SBException

    @property
    def dots(self):     #точки корабля
        if self.length == 1:
            return [Dot(self.x, self.y)]
        else:
            dots = [Dot(self.x, self.y), Dot(self.x_end, self.y_end)]
            if self.length == 3:
                dots.append(Dot(int((self.x+self.x_end)/2), int((self.y+self.y_end)/2)))
            return dots

class Polygon:                                      #назвал Полигоном вместо боард, так вышло
    def __init__(self):
        self.poly = [[' o ' for x in range(7)] for y in range(7)]
        for i in range(7):
            self.poly[0][i] = ' ' + str(i) + ' '
            self.poly[i][0] = str(i)
        self.poly[0][0] = ' '
        self.shot_hits = 0
        self.ships = []

    def get_poly(self):
        for i in self.poly:
            print('|'.join(i))

    def get_poly_invis(self):
        for i in self.poly:
            s = '|'.join(i)
            print(s.replace(' ■ ', ' o '))

    def check_ship(self,ship):                  #проверка на соседство кораблей
        neig = [(-1,-1), (-1,0), (-1, 1),
                (0,-1), (0,0), (0, 1),
                (1,-1), (1,0), (1, 1)]
        for d in ship.dots:
            for i in neig:
                try:
                    if self.poly[d.x+i[0]][d.y+i[1]] == ' ■ ':
                        return False
                except IndexError:
                    pass
        return True

    def add_ship(self, ship):
        self.ships.append(ship)
        for i in ship.dots:
            self.poly[i.x][i.y] = ' ■ '

    def fire(self, dot):
        if (1 > dot.x or dot.x > 6) or (1 > dot.y or dot.y > 6):
            raise PolygonOutException
        if self.poly[dot.x][dot.y] == ' ■ ':
            self.poly[dot.x][dot.y] = ' x '
            self.shot_hits += 1
            return True
        elif self.poly[dot.x][dot.y] == ' T ' or self.poly[dot.x][dot.y] == ' x ':
            raise PolygonRepeatedShot
        else:
            self.poly[dot.x][dot.y] = ' T '
        print('НЕ ПОПАЛ')
        return False

class Game:
    def __init__(self):
        self.p = None
        self.me = self.creat_polygon()          #создание доски игрока
        self.ai = self.creat_polygon()          #создание доски копьютера

    def greet(self):
        print(' '*25,"-------------------")
        print(' '*25,"  Приветсвуем вас  ")
        print(' '*25,"      в игре       ")
        print(' '*25,"    морской бой    ")
        print(' '*25,"-------------------")
        print(' '*25," формат ввода: x y ")
        print(' '*25," x - номер строки  ")
        print(' '*25," y - номер столбца ")
        print("_"*69)
        print()

    def creat_polygon(self):                #добавление в доску по очередно кораблей
        lens = [3, 2, 2, 1, 1, 1, 1]        #код длинный потому что иногда происходит
        count_ships = 0                     #бесконичный цикл при добавление последного корабля
        while count_ships != 7:             #из-за условия соседства, поэтому такой перебор
            self.p = Polygon()
            count_ships = 0
            for l in lens:
                count = 0
                while count < 3600:
                    orient = randint(0, 1)
                    if orient == 0:
                        x = randint(1, 6)
                        y = randint(1, 7 - l)
                        x_end = x
                        y_end = y + l - 1
                        s = Ship(x, y, l, x_end, y_end)
                        if self.p.check_ship(s):
                            self.p.add_ship(s)
                            count_ships += 1
                            break
                    else:
                        x = randint(1, 7 - l)
                        y = randint(1, 6)
                        x_end = x + l - 1
                        y_end = y
                        s = Ship(x, y, l, x_end, y_end)
                        if self.p.check_ship(s):
                            self.p.add_ship(s)
                            count_ships += 1
                            break
                    count += 1
        return self.p

    def get_me_ai(self):            # вывод моей доски и доски компа в одну строку, а не поочередно
        print(' '*8 + 'Твое ПОЛЕ' + ' '*37 + 'ПОЛЕ ИИ')
        print(' ' + '_'*23 + ' '*22 + '_'*23)
        me = iter(self.me.poly)
        ai = iter(self.ai.poly)
        for i in range(7):
            str_me = '|'.join(next(me))
            str_ai = '|'.join(next(ai)).replace(' ■ ', ' o ')
            print(str_me + ' '*20 + str_ai)

    def shot(self, poly, pl):       #выстрел до тех пор пока попадает
        self.b = True
        while self.b:
            try:
                self.b = poly.fire(pl.ask())
            except PolygonOutException as a:
                print(a)
                continue
            except PolygonRepeatedShot as e:
                if not isinstance(pl, AI):
                    print(e)
                continue
            else:
                if poly.shot_hits == 11:
                    self.get_me_ai()
                    break
                if self.b == True:
                    print('GOOD SHOT, стреляй еще раз')
                    self.get_me_ai()

class Player:           #копи паст
    def ask(self):
        ...

class AI(Player):
    def __init__(self):
        self.dots = []

    def ask(self):
        d = Dot(randint(1, 6), randint(1, 6))
        print(f"Ход компьютера: {d.x} {d.y}")
        return d

class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()
            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue
            x, y = cords
            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите числа! ")
                continue
            x, y = int(x), int(y)
            return Dot(x, y)

g = Game()
g.greet()
me_fire = User()
ai_fire = AI()

for i in range(26):
    g.get_me_ai()
    # print('-'*24)
    # g.ai.get_poly()         #ЧИТ!!
    g.shot(g.ai, me_fire)
    if g.ai.shot_hits == 11:
        print()
        print("YOU WIN, Сongratulations!!!")
        break
    g.shot(g.me, ai_fire)
    if g.me.shot_hits == 11:
        print("\nAI WON, unfortunately!!!")
        break
    print('=' * 69)













