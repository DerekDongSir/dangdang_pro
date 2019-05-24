class Item(object): #商品项类，属性为书籍对象以及书籍数量
    def __init__(self,book,num):
        self.book = book
        self.book_num = num
        self.status = True #如果被用户点击删除，则状态置为 False
        self.price = "%.1f"%(self.book.dangdang_price * self.book_num)

class Cart(object):
    def __init__(self):
        self.total_cost =0
        self.saving_cost =0
        self.cart_items = {}


    def update_cost(self):
        self.total_cost = sum([item.book_num * item.book.dangdang_price for item in self.cart_items.values() if item.status])
        self.saving_cost = sum([item.book_num*(item.book.marketing_price - item.book.dangdang_price) for item in self.cart_items.values() if item.status])


    def add_item(self,item): #形参 item 为要添加的书籍项，如果该项已存在，则更新其数量
        if self.cart_items.get(item.book.id):
            self.cart_items[item.book.id].book_num += item.book_num
        else:
            self.cart_items[item.book.id] = item
        self.update_cost() #添加完书籍后对总价和节省支出进行更新


    def remove_item(self,book_id): #book_id 为键,此时只是将 status置为 False,不是真正的移除
        if self.cart_items.get(book_id):
            self.cart_items[book_id].status = False
            self.update_cost() #更新cost


    def update_cart(self): #更新购物车,将 status为 False的商品清除
        self.cart_items = {key:val for key,val in self.cart_items.items() if val.status }
        self.update_cost() #更行 cost


    def book_num_adjust(self,book_id,number): # 对书籍数量进行调整，如果调整后的数量小于1 则置为1
        """
        实现两种需求，书籍数量的调整，以及将数据的状态恢复
        :param book_id:
        :param number:
        :return:
        """
        temp = self.cart_items.get(book_id)
        if temp:
            temp.status = True #
            temp.book_num = number if number >0 else temp.book_num
            self.update_cost()#更新cost

