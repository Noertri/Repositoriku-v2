class Rectangle:

    def __init__(self, w, h):
        self.width = w
        self.height = h

    def set_width(self, w):
        self.width = w

    def set_height(self, h):
        self.height = h

    def get_area(self):
        return self.height*self.width

    def get_perimeter(self):
        return 2*self.width + 2*self.height

    def get_diagonal(self):
        diag = ((self.width**2) + (self.height**2))**0.5
        return diag

    def get_picture(self):
        h = int(self.height)
        w = int(self.width)

        if (h < 50) and (w < 50):
            lines = ""
            for i in range(h):
                lines += "{}\n".format('*'*w)
            return lines
        else:
            return "Too big for picture."

    def get_amount_inside(self, shape):
        w = shape.width
        h = shape.height

        if (w <= self.width) and (h <= self.height):
            m = self.width//w
            n = self.height//h
            return m*n
        else:
            return 0

    def __repr__(self):
        return f"Rectangle(width={self.width}, height={self.height})"


class Square(Rectangle):

    def __init__(self, side):
        self.side = side
        super().__init__(side, side)

    def set_side(self, s):
        self.side = s
        super().set_width(s)
        super().set_height(s)

    def set_height(self, s):
        self.side = s
        super().set_height(s)
        super().set_width(s)

    def set_width(self, s):
        self.side = s
        super().set_height(s)
        super().set_width(s)

    def __repr__(self):
        return f"Square(side={self.side})"


rect = Rectangle(10, 5)
print(rect.get_area())
rect.set_height(55)
print(rect.get_perimeter())
print(rect)
print(rect.get_picture())