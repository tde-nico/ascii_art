import pygame as pg
import pygame.gfxdraw
import numpy as np
import cv2


class ArtConverter:
	def __init__(self, path, pixel_size=7, color_lvl=8):
		pg.init()
		self.path = path
		self.pixel_size = pixel_size
		self.color_lvl = color_lvl
		self.image = self.get_image()
		self.RES = self.WIDTH, self.HEIGHT = self.image.shape[0], self.image.shape[1]
		self.surface = pg.display.set_mode(self.RES)
		self.clock = pg.time.Clock()
		self.palette, self.color_coeff = self.create_palette()

	def draw_converted_image(self):
		color_indices = self.image // self.color_coeff
		for x in range(0, self.WIDTH, self.pixel_size):
			for y in range(0, self.HEIGHT, self.pixel_size):
				color_key = tuple(color_indices[x, y])
				if sum(color_key):
					color = self.palette[color_key]
					pygame.gfxdraw.box(self.surface, (x, y, self.pixel_size, self.pixel_size), color)

	def create_palette(self):
		colors, color_coeff = np.linspace(0, 255, num=self.color_lvl, dtype=int, retstep=True)
		color_palette = [np.array([r, g, b]) for r in colors for g in colors for b in colors]
		palette = {}
		color_coeff = int(color_coeff)
		for color in color_palette:
			color_key = tuple(color // color_coeff)
			palette[color_key] = color
		return palette, color_coeff

	def get_image(self):
		self.cv2_image = cv2.imread(self.path)
		transposed_image = cv2.transpose(self.cv2_image)
		image = cv2.cvtColor(transposed_image, cv2.COLOR_BGR2RGB)
		return image

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

