def total_sum(*args):
	sum = 0
	for num in args:
		sum += num
	return sum


sum = total_sum(3, 6, 7, 8, 2)
print("Sum :", sum)


def test_args(*args):
	for key, value in args[2].items():
		print(str(key)+' : '+str(value))


test_dict = {
	"brand": "Ford", 
	"model": "Mustang", 
	"year": 1964
}

args = test_args(3, 2, test_dict)
# print("Args :", args)

def print_kwargs(**kwargs):
	print("kwargs :", kwargs)

	for key in kwargs:
		print("The key {} holds {} value".format(key, kwargs[key]))


print_kwargs(a=1, b=2, c="Some Text")

def function( *args, **kwargs):
	print("args : ", args)
	print("kwargs : ", kwargs)


function(6, 7, 8, a=1, b=2, c="Some Text")
