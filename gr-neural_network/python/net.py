from torch import nn

class feed_forward(nn.Module):

	def __init__(self, input, output):

		super(feed_forward, self).__init__()

		self.lin1 = nn.Linear(input, 30)
		self.act1 = nn.ReLU()
		self.lin2 = nn.Linear(30, output)


	def forward(self, data):

		data = self.lin1(data)
		data = self.act1(data)
		data = self.lin2(data)

		return data