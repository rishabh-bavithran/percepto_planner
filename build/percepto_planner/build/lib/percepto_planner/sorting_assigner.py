#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from pplanner_interfaces.msg import ArucoDataset
from pplanner_interfaces.msg import ArucoData

class SortingAssigner(Node):
    def __init__(self):
        super().__init__("sorting_assigner")
        self.get_logger().info("Sorting Assigner Node has started")
        self.robots_list = self.create_subscription(ArucoDataset,"robots", self.callback_robots_arucodataset, 10 )
        self.objects_list = self.create_subscription(ArucoDataset, "objects", self.calback_objects_arucodataset, 10)
        self.robots_total_count = 1
        self.objects_total_count = 1
        self.robots_list_global = ArucoDataset()
        self.objects_list_global = ArucoDataset()
        self.robots_status = []
        self.objects_status = []
        #self.robot_number = []
        self.i = 0
        self.j = 0 
        self.assigning_timer = self.create_timer(0.5, self.assigning_timer_callback)

    def calback_objects_arucodataset(self,msg):
        if len(msg.dataset) == self.objects_total_count and self.j == 0:
            #self.get_logger().info("Object count has been verified")
            if self.j == 0:
                self.objects_list_global = msg  
                object_status_track = 0
                while object_status_track < self.objects_total_count:
                    self.objects_status.append("Unpicked") 
                    object_status_track += 1
                self.j += 1

    def callback_robots_arucodataset(self ,msg):
        #self.get_logger().info(str(msg.dataset))
        if len(msg.dataset) == self.robots_total_count and self.i == 0:
            #self.get_logger().info("Robot count has been verified")
            if self.i == 0:
                self.robots_list_global = msg  
                robot_status_track = 0
                while robot_status_track < self.robots_total_count:
                    self.robots_status.append("Ready") 
                    robot_status_track += 1
                self.i += 1


    def assigning_timer_callback(self):
        if self.robots_list_global.dataset and self.objects_list_global.dataset:
            #self.get_logger().info("Robot list has been assigned once")
            #self.get_logger().info(str(self.robots_list_global))
            #self.get_logger().info(str(self.robots_status))
            if "Ready" in self.robots_status:
                self.get_logger().info("STARTED ASSIGNING ROBOTS TO OBJECTS")
                if "Unpicked" in self.objects_status:
                    robot_ready_index = self.robots_status.index("Ready")
                    object_unpicked_indices = [o for o, x in enumerate(self.robots_status) if x == "Unpicked"]
                    #object_unpicked_index = self.objects_status.index("Unpicked")
                    self.get_logger().info(str(robot_ready_index))
                    robot_assignment = ArucoData()
                    object_assignment = ArucoData()
                    robot_assignment = self.robots_list_global.dataset[robot_ready_index]
                    #object_assignment = self.objects_list_global.dataset[object_unpicked_index]
                    #object_ready_index_tracker = 0
                    closest_object_distance = 100000
                    # while object_ready_index_tracker <= object_unpicked_indices:
                    #     object_assignment = self.objects_list_global.dataset[]

                    for object_unpicked_index in object_unpicked_indices:
                        self.get_logger().info("FINDING CLOSEST DISTANCE")
                        object_assignment = self.objects_list_global.dataset[object_unpicked_index]
                        distance = abs((robot_assignment.x_data - object_assignment.x_data)**2 + 
                                       (robot_assignment.y_data - object_assignment.y_data)**2) 

                        if distance < closest_object_distance: 
                              closest_object_distance = distance
                              final_object_index = object_unpicked_index

                        assigned_object = self.objects_list_global[final_object_index]
                        self.get_logger().info(str(assigned_object))

                    
                    self.get_logger().info("Assignment has been completed")
                    #self.get_logger().info("Robot ID " + str(robot_assignment.id_data) + "has been assigned to Object with ID" + str(assigned_object.id_data))

                        
                    

                        



            # status_track =len(self.robots_list_global.dataset)
            # status_track_variable = 0 
            # while status_track_variable < status_track:
            #     self.robots_status.append("Ready")


            

            # robot = ArucoData()
            # robot.id_data = self.robots_list_global.dataset
            # self.get_logger().info("ID DATA that has been saved : ", str(robot.id_data))

            #self.get_logger().info(self.robots_status[0])
            
    # def robots_initial_state_setup(self, robot_data):
        
    #     self.get_logger().info(str(robot_data.dataset))
    #     #self.get_logger().info("New function")
    #     robot = ArucoData()

    #     i = 0

    #     while i<len(robot_data):
    #         robot = robot_data[i].dataset
    #         robot.status = "Ready"











        



def main(args=None):
    rclpy.init(args=args)
    node = SortingAssigner()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
