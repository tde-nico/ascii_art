import pygame as pg
import numpy as np
import cv2


ASCII_CHARS = ' Ixzao*#MW&8%B@$'
ASCII_COEFF = 255 // (len(ASCII_CHARS) - 1)


class ArtConverter:
	def __init__(self, path, font_size=12, color_lvl=8):
		pg.init()
		self.path = path
		self.color_lvl = color_lvl
		self.image, self.gray_image = self.get_image()
		self.RES = self.WIDTH, self.HEIGHT = self.image.shape[0], self.image.shape[1]
		self.surface = pg.display.set_mode(self.RES)
		self.clock = pg.time.Clock()

		self.font = pg.font.SysFont('Courier', font_size, bold=True)
		self.char_step = int(font_size * 0.6)
		self.palette, self.color_coeff = self.create_palette()

	def draw_converted_image(self):
		char_indices = self.gray_image // ASCII_COEFF
		color_indices = self.image // self.color_coeff
		for x in range(0, self.WIDTH, self.char_step):
			for y in range(0, self.HEIGHT, self.char_step):
				char_index = char_indices[x, y]
				if char_index:
					char = ASCII_CHARS[char_index]
					color = tuple(color_indices[x, y])
					self.surface.blit(self.palette[char][color], (x,y))

	def create_palette(self):
		colors, color_coeff = np.linspace(0, 255, num=self.color_lvl, dtype=int, retstep=True)
		color_palette = [np.array([r, g, b]) for r in colors for g in colors for b in colors]
		palette = dict.fromkeys(ASCII_CHARS, None)
		color_coeff = int(color_coeff)
		for char in palette:
			char_palette = {}
			for color in color_palette:
				color_key = tuple(color // color_coeff)
				char_palette[color_key] = self.font.render(char, False, tuple(color))
			palette[char] = char_palette
		return palette, color_coeff

	def get_image(self):
		self.cv2_image = cv2.imread(self.path)
		transposed_image = cv2.transpose(self.cv2_image)
		image = cv2.cvtColor(transposed_image, cv2.COLOR_BGR2RGB)
		gray_image = cv2.cvtColor(transposed_image, cv2.COLOR_BGR2GRAY)
		return image, gray_image

	def draw_cv2_image(self):
		resized_cv2_image = cv2.resize(self.cv2_image, (640,360), interpolation=cv2.INTER_AREA)
		cv2.imshow('img', resized_cv2_image)

	def draw(self):
		#pg.surfarray.blit_array(self.surface, self.image)
		self.surface.fill('black')
		self.draw_converted_image()
		self.draw_cv2_image()

	def save_image(self):
		pygame_image = pg.surfarray.array3d(self.surface)
		cv2_img = cv2.transpose(pygame_image)
		cv2.imwrite('test.jpg', cv2_img)

	def run(self):
		while True:
			for event in pg.event.get():
				if event.type == pg.QUIT:
					exit()
				elif event.type == pg.KEYDOWN:
					if event.key == pg.K_s:
						self.save_image()
			self.draw()
			pg.display.set_caption(str(self.clock.get_fps()))
			pg.display.flip()
			self.clock.tick(60)


if __name__ == '__main__':
	app = ArtConverter('img/car.jpg')
	app.run()

