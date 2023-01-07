import pygame as pg
import cv2

ASCII_CHARS = '.",:;!~+-xmo*#W&8@'
ASCII_COEFF = 255 // (len(ASCII_CHARS) - 1)

class ArtConverter:
	def __init__(self, path, font_size=12):
		pg.init()
		self.path = path
		self.image = self.get_image()
		self.RES = self.WIDTH, self.HEIGHT = self.image.shape[0], self.image.shape[1]
		self.surface = pg.display.set_mode(self.RES)
		self.clock = pg.time.Clock()

		self.font = pg.font.SysFont('Courier', font_size, bold=True)
		self.char_step = int(font_size * 0.6)
		self.render_ascii_chars = [
			self.font.render(char, False, 'white') for char in ASCII_CHARS
		]

	def draw_converted_image(self):
		char_indices = self.image // ASCII_COEFF
		for x in range(0, self.WIDTH, self.char_step):
			for y in range(0, self.HEIGHT, self.char_step):
				char_index = char_indices[x, y]
				if char_index:
					self.surface.blit(self.render_ascii_chars[char_index], (x,y))

	def get_image(self):
		self.cv2_image = cv2.imread(self.path)
		transposed_image = cv2.transpose(self.cv2_image)
		gray_image = cv2.cvtColor(transposed_image, cv2.COLOR_BGR2GRAY)
		return gray_image

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

