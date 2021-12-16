'''
    Sau khi tìm hiểu yêu câu bài toán, tôi tiến hành phân tích như sau:
        1.  Thang máy có thể đi lên hoặc đi xuống và sẽ dừng lại ở tầng mà người sử dụng yêu cầu.
        2.  Nếu thang máy nhận dược yêu cầu đi xuống trong khi đang đi lên thì nó sẽ đi lên tầng cao nhất đối với yêu cầu hiện tai rồi mới đi xuống
        3.  Người sử dụng có thể gửi request bất kì lúc nào.
        4.  Thang máy hoạt động sẽ ưu tiên về khoảng cách thay vì thời gian. Có nghĩa là, giả sử nếu thang máy, người A và người B đang ở tầng 1, người A nhấn nút đi lên tầng 4,
        sau đó người B nhấn nút để đi lên tầng 2. Tuy người A yêu cầu thang máy trước nhưng thang máy sẽ không đi lên tầng 4 rồi xuống lại tầng 2 mà sẽ dùng
        lại ở tầng 2 để người B ra ngoài sau đó đi lên tầng 4. Do đó, yêu cầu sẽ được ưu tiên theo khoảng cách thay vì ưu tiên theo thời gian.
    ý tưởng:
        ở đây tôi giả sử là yêu cầu đi lên sẽ được ưu tiên hơn yêu cầu thi xuống. Điều đó có nghĩa rằng khi thang máy đang ở tình trạng chờ, 
        nếu 2 trường hợp đi lên và đi xuống được yêu cầu cùng lúc thì yêu cầu đi lên sẽ được ưu tiên hơn.
        Sử dụng OOP để giải quyết bài toán:
            1.  Thiết kết lớp Resquest, lớp Elevator để đại diện cho các instance trong thực tế.
            2.  Sử dụng cấu trúc dữ liệu hàng đợi ưu tiên (PriorityQueue) để lưu và xử lý các request vì ở đây ưu tiên theo khoảng cách giữa tầng hiện tại vs kế tiếp
            3.  Sử dụng priorityQueue để lưu các yêu cầu đi xuống và sắp xếp chúng dựa theo tầng mong muốn đến. Tương tự, tôi cũng sử dụng priorityQueue để lưu các yêu
            đi lên và sắp xếp theo tầng mong muốn đến
            4. Khi mà người sử dụng thang máy yêu cầu ở bên ngoài thì thang máy dừng lại tại tầng hiện tại của người gửi yêu cầu để pickup người đó vào thang máy trước
            khi tiếp tục đi đến desired floor.
            5.  Trong quá trình vận chuyển hành khách, nhờ vào cấu trúc dữ liệu hàng đợi ưu tiên mà thuật toán có thẻ nhận và trả khách theo đường tối ưu.
        UP: đi lên
        DOWN: đi xuông
        IDLE: trạng thái chờ
        IN: trong thang máy
        OUT: ngoài thang máy
'''


from queue import PriorityQueue

class Resquest():
    def __init__(self,currentFLoor, desiredFloor, direction, location):
        self.currentFloor = currentFLoor #tầng hiện tại
        self.desiredFloor = desiredFloor #tầng muốn đến
        self.direction = direction #hướng (đi lên or đi xuống)
        self.location = location #vi tri trong hay ngoai thang may

#Thiết kế lớp ResUp kế thừa từ lớp Resquest
class ResUp(Resquest):
    #Hàm tinh chỉnh hàm so sánh của PriorityQueue
    def __lt__(self, other):
        return self.desiredFloor - other.desiredFloor < 0

#Thiết kế lớp ResDown kế thừa từ lớp Resquest
class ResDown(Resquest):
    # Hàm tinh chỉnh hàm so sánh của PriorityQueue
    def __lt__(self, other):
        return self.desiredFloor - other.desiredFloor > 0

class Elevator():
    def __init__(self, currentFloor):
        self.upQueue = PriorityQueue()
        self.downQueue = PriorityQueue()
        self.currentFLoor = currentFloor

        #Khởi tạo trang thái ban đầu là 'IDLE'
        self.directon = 'IDLE'


    def sendUpResquest(self, upRequest):
        '''
            Nếu như yêu cầu được gửi từ bên ngoài của thang máy thì dùng lại tại tầng hiện tại của yêu cầu được gửi đi, và tiếp tục di chuyển đến desired floor
        '''
        if(upRequest.location == 'OUT'):
            req = ResUp(upRequest.currentFloor, upRequest.currentFloor, 'UP', 'OUT')
            self.upQueue.put(req)
            print('Them 1 yeu cau di len tang: ' + str(upRequest.currentFloor))
        '''
            Nếu như yêu cầu được gửi từ bên trong của thang máy thì dùng lại tại tầng hiện tại của yêu cầu được gửi đi, và tiếp tục di chuyển đến desired
        '''

        self.upQueue.put(upRequest)
        print('Them 1 yeu cau di len tang: ' + str(upRequest.desiredFloor))

    def sendDownResquest(self, downRequest):
        '''
        Nếu như yêu cầu được gửi từ bên ngoài của thang máy thì dùng lại tại tầng hiện tại của yêu cầu được gửi đi, và tiếp tục di chuyển đến desired floor
        '''
        if(downRequest.location == 'OUT'):
            req = ResDown(downRequest.currentFloor, downRequest.currentFloor, 'DOWN', 'OUT')
            self.downQueue.put(req)
            print('Them 1 yeu cau di xuong tang: ' + str(downRequest.currentFloor))
        '''
            Nếu như yêu cầu được gửi từ bên trong của thang máy thì dùng lại tại tầng hiện tại của yêu cầu được gửi đi, và tiếp tục di chuyển đến desired floor
        '''
        self.downQueue.put(downRequest)
        print('Them 1 yeu cau di xuong tang: ' + str(downRequest.desiredFloor))

    def UpResquest(self):
        while(not self.upQueue.empty()):
            upResquest = self.upQueue.get()
            self.currentFLoor = upResquest.desiredFloor
            print('Thang may dang di len va dung lai tai tang ' + str(self.currentFLoor))
        if(not self.downQueue.empty()): #nếu hàng đợi downQueue không rỗng thì thang máy bắt đầu đi xuống
            self.directon = 'DOWN'
        else: #Ngược lại thì thang máy dừng lại
            self.directon = 'IDLE'
    def DownResquest(self):
        while(not self.downQueue.empty()):
            downResquest = self.downQueue.get()
            self.currentFLoor = downResquest.desiredFloor
            print('Thang may dang di xuong va dung lai lai tai tang ' + str(self.currentFLoor))
        if(not self.upQueue.empty()): #Nếu hàng đợi upQueue không rỗng thì thang máy bắt đầu đi lên
            self.directon = 'UP'
        else: #Ngược lại thì thang máy dừng lại
            self.directon = 'IDLE'
    def processResquest(self):
        if(self.directon == 'UP' or self.directon == 'IDLE'):
            self.UpResquest()
            self.DownResquest()
        else:
            self.DownResquest()
            self.UpResquest()
    def main(self):
        while(not self.upQueue.empty() or not self.downQueue.empty()):
            self.processResquest()
        print('ĐÃ CHỞ XONG HÀNH KHÁCH!!!!!!')
        self.directon = 'IDLE'
if __name__ == '__main__':
    elevator = Elevator(0)
    requestUp_1 = ResUp(elevator.currentFLoor, 5, 'UP', 'IN')
    requestUp_2 = ResUp(elevator.currentFLoor, 3, 'UP', 'IN')

    requestDown_1 = ResDown(elevator.currentFLoor, 1, 'DOWN', 'IN')
    requestDown_2 = ResDown(elevator.currentFLoor, 3, 'DOWN', 'IN')
    requestDown_3 = ResDown(2, 0, 'DOWN', 'OUT')

    #Giả sử có 2 người ở trong thang máy thực hiện 2 yêu cầu requestUp_1 và RequestUp_2
    elevator.sendUpResquest(upRequest=requestUp_1)
    elevator.sendUpResquest(upRequest=requestUp_2)

    #Giả sử 1 người ở bên ngoài tầng 4 thực hiên yêu cầu requestDown_3
    elevator.sendDownResquest(downRequest=requestDown_3)

    #Giả sử 2 người ở bên trong thang m áythực hiên 2 yêu cầu requestDown_1 v requestDown_2
    elevator.sendDownResquest(downRequest=requestDown_1)
    elevator.sendDownResquest(downRequest=requestDown_2)

    elevator.main()


