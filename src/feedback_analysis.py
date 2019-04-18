#!/usr/bin/env python
#author amir sharifi

import rospy
from mrl_srvs.msg import RobotsFeedback
from matplotlib import pyplot as plt 
import xlsxwriter
from datetime import datetime
import itertools
import os

node_name = 'robot_feedback_analysis'


class FeedBackAnalysis:
    def __init__(self,sub_topic):
        rospy.Subscriber(sub_topic,RobotsFeedback,self._callback)
        self.start_time = rospy.get_time()
        # self.current_right = []
        # self.current_left = []
        # self.current_sum = []
        self.robot_currents = []
        self.robot_torque = []
        self.duration = []
    def _callback(self,robotfeedback):
        """
        get karo_feedBack topic and set sum important param
        @param current dic{key:value}
        @param key of current dic : current right,current left,current joint0,current joint1,current joint2,current joint3
        @param key of torque_dic : torque right,torque left,torque joint0,torque joint1,torque joint2,torque joint3
        """
        # self.current_left.append(robotfeedback.current_left)
        # self.current_right.append(robotfeedback.current_right)
        # self.current_sum.append(robotfeedback.current_left + robotfeedback.current_right)
        
        current = {'current_right':robotfeedback.current_right,\
            'current_left':robotfeedback.current_left,\
                'current_sum':robotfeedback.current_sum,\
                    'current_joint0':robotfeedback.current_joint0,\
                        'current_joint1':robotfeedback.current_joint1,\
                            'current_joint2':robotfeedback.current_joint2}

        torque = {'torque_right': robotfeedback.torque_right,\
            'torque_left':robotfeedback.torque_left,\
                    'torque_joint0':robotfeedback.torque_joint0,\
                        'torque_joint1':robotfeedback.torque_joint1,\
                            'torque_joint2':robotfeedback.torque_joint2}
        
        self.robot_currents.append(current)
        self.robot_torque.append(torque)
        secs_start = rospy.get_time() - self.start_time
        self.duration.append(secs_start)
        
    def initExelParam(self,path_file):
        date = datetime.now()
        self.exel_file_name = path_file + date.strftime("%Y-%m-%d-%H:%M") +'.xlsx'
        self.workbook = xlsxwriter.Workbook(self.exel_file_name)
        self.worksheet = self.workbook.add_worksheet()
        bold = self.workbook.add_format({'bold': 1})
        self.worksheet.write('A1', 'Time_start', bold)
        self.worksheet.write('B1', 'Current_Right', bold)
        self.worksheet.write('C1', 'Current_Left', bold)
        self.worksheet.write('D1', 'Current_Right+Left', bold)
        self.worksheet.write('E1', 'Current_Yaw',bold)
        self.worksheet.write('F1','Current_Link1',bold)
        self.worksheet.write('G1','Current_Link2',bold)
        self.worksheet.write('H1','Torque Right',bold)
        self.worksheet.write('I1','Torque Left',bold)
        self.worksheet.write('J1','Torque Yaw',bold)
        self.worksheet.write('K1','Torque Link1',bold)
        self.worksheet.write('L1','Torque Link2',bold)
        self.row = 1

    def writeExelFile(self,time,current_list,torque_list):
        """
        @param Current Dic is a list of all current of joint and traction
        @param Torque_Dic is a list of all torque of joint and traction
        @param time is a list of time from start package
        """
        try:
            col = 0
            for current_dic, torque_dic, sec in zip(current_list,torque_list,time):
                current_dic = dict(current_dic)
                torque_dic = dict(torque_dic)
                # print(torque_dic.get('torque_left'))
                self.worksheet.write(self.row,col,sec)
                self.worksheet.write(self.row, col + 1, current_dic.get('current_right'))
                self.worksheet.write(self.row,col + 2 , current_dic.get('current_left'))
                self.worksheet.write(self.row,col + 3 , current_dic.get('current_sum'))
                self.worksheet.write(self.row,col + 4 , current_dic.get('current_joint0'))
                self.worksheet.write(self.row,col + 5 , current_dic.get('current_joint1'))
                self.worksheet.write(self.row,col + 6 , current_dic.get('current_joint2'))
                

                self.worksheet.write(self.row,col + 7 , torque_dic.get('torque_right'))
                self.worksheet.write(self.row,col + 8 , torque_dic.get('torque_left'))
                self.worksheet.write(self.row,col + 9 , torque_dic.get('torque_joint0'))
                self.worksheet.write(self.row,col + 10, torque_dic.get('torque_joint1'))
                self.worksheet.write(self.row,col + 11, torque_dic.get('torque_joint2'))
                self.row += 1
        except Exception as e:
            rospy.logwarn('Exel File Not Write Currectly {}'.format(e))
        
        finally:
            self.workbook.close()
            rospy.logwarn('Exel File Write Currectly to ' + self.exel_file_name)

    def drow_plt(self,time,current_list,torque_list,path_to_save,mode = 'all'):
        """
        @param mode
        current_traction current_manipulator torque_traction torque_manipulator
        if use all all of those work together
        """
        current_left = []
        current_right = []
        current_joint0 = []
        current_joint1 = []
        current_joint2 = []
        current_sum = []

        torque_left = []
        torque_right = []
        torque_sum = []
        torque_joint0 = []
        torque_joint1 = []
        torque_joint2 = []
        for current_dic,torque_dic in zip(current_list,torque_list):
            current_dic = dict(current_dic)
            torque_dic = dict(torque_dic)
            current_left.append(current_dic.get('current_left'))
            current_right.append(current_dic.get('current_right'))
            current_sum.append(current_dic.get('current_sum'))
            current_joint0.append(current_dic.get('current_joint0'))
            current_joint1.append(current_dic.get('current_joint1'))
            current_joint2.append(current_dic.get('current_joint2'))

            torque_left.append(torque_dic.get('torque_left'))
            torque_right.append(torque_dic.get('torque_right'))
            torque_sum.append(torque_dic.get('torque_left') + torque_dic.get('torque_right'))
            torque_joint0.append(torque_dic.get('torque_joint0'))
            torque_joint1.append(torque_dic.get('torque_joint1'))
            torque_joint2.append(torque_dic.get('torque_joint2'))
        
        if mode == 'current_traction' or mode == 'all':
            fig_current_traction = plt.figure(1)
            plt.subplot(311)
            plt.title("3 Plot of traction current in time data")  
            plt.ylabel('Current Left')
            plt.plot(time,current_left)

            plt.subplot(312)
            plt.ylabel('Curent Right')
            plt.plot(time,current_right)

            plt.subplot(313)
            plt.xlabel('Time')
            plt.ylabel('Current Sum')
            plt.plot(time,current_sum)
            fig_current_traction.savefig(fname = path_to_save + 'current_traction.pdf',format = 'pdf',dpi = 150, quality = 100 , bbox_inches='tight')
            fig_current_traction.savefig(fname = path_to_save + 'current_traction.png',format = 'png',dpi = 150, quality = 100 , bbox_inches='tight')
            # plt.show()

        if mode == 'current_manipulator' or mode == 'all' :
            
            fig2 = plt.figure(2)
            plt.subplot(311)
            plt.title("3 Plot of manipulator current in time")
            plt.ylabel('Current Yaw')
            plt.plot(time,current_joint0)
            1
            plt.subplot(312)
            plt.ylabel('Current Link1')
            plt.plot(time,current_joint1)

            plt.subplot(313)
            plt.xlabel('Time')
            plt.ylabel('Current Link2')
            plt.plot(time,current_joint2)
            fig2.savefig(fname = path_to_save + 'current_manipulator.pdf',format = 'pdf',dpi = 150, quality = 100 , bbox_inches='tight')
            fig2.savefig(fname = path_to_save + 'current_manipulator.png',format = 'png',dpi = 150, quality = 100 , bbox_inches='tight')
            # plt.show()
        
        if mode == 'torque_traction' or mode == 'all':
            fig3 = plt.figure(3)
            plt.subplot(311)
            plt.title("3 Plot of traction_torque in time data")  
            plt.ylabel('Torque Left')
            plt.plot(time,torque_left)

            plt.subplot(312)
            plt.ylabel('Torque Right')
            plt.plot(time,torque_right)

            plt.subplot(313)
            plt.xlabel('Time')
            plt.ylabel('Torque Sum')
            plt.plot(time,torque_sum)
            fig3.savefig(fname = path_to_save + 'torque_traction.pdf',format = 'pdf',dpi = 150, quality = 100 , bbox_inches='tight')
            fig3.savefig(fname = path_to_save + 'torque_traction.png',format = 'png',dpi = 150, quality = 100 , bbox_inches='tight')
            # plt.show()

        if mode == 'torque_manipulator' or mode == 'all':
            fig4 = plt.figure(4)
            plt.subplot(311)
            plt.title("3 Plot of torque_manipulator in time data")  
            plt.ylabel('Torque Yaw')
            plt.plot(time,torque_joint0)

            plt.subplot(312)
            plt.ylabel('Torque Link1')
            plt.plot(time,torque_joint1)

            plt.subplot(313)
            plt.xlabel('Time')
            plt.ylabel('Torque Link2')
            plt.plot(time,torque_joint2)
            fig4.savefig(fname = path_to_save + 'torque_manipulator.pdf',format = 'pdf',dpi = 150, quality = 100 , bbox_inches='tight')
            fig4.savefig(fname = path_to_save + 'torque_manipulator.png',format = 'png',dpi = 150, quality = 100 , bbox_inches='tight')
            # fig4.show()

    @staticmethod
    def spin():
        rospy.spin()


def main():
    feed_back_topic = rospy.get_param(node_name + '/robot_feedback_topic','/karo_feedback')
    feed_back_analysis = FeedBackAnalysis(feed_back_topic)
    path_file =  rospy.get_param(node_name + '/path_to_save_data','/home/opst/catkin_ws/src/mrl_robots_feedback/data/')
    exel_is_enable = rospy.get_param(node_name + '/exel_is_enable', True)
    plot_is_enable = rospy.get_param(node_name + '/plot_is_enable', True)
    plot_mode = rospy.get_param(node_name + '/plot_mode','all')
    date = datetime.now()
    dir_name = date.strftime("%Y-%m-%d-%H:%M")
    os.mkdir(path_file + dir_name)
    dir_path = path_file + dir_name + '/'
    try:
        feed_back_analysis.spin()
        rospy.signal_shutdown(node_name + ' is Shoting down wait for plt')
    except rospy.ROSInterruptException:
        rospy.logerr("program interrupted before completion") 
    finally:
        if exel_is_enable:
            feed_back_analysis.initExelParam(dir_path)
            feed_back_analysis.writeExelFile(feed_back_analysis.duration,feed_back_analysis.robot_currents,feed_back_analysis.robot_torque)
        if plot_is_enable:
            feed_back_analysis.drow_plt(feed_back_analysis.duration,feed_back_analysis.robot_currents,feed_back_analysis.robot_torque,dir_path,plot_mode)
if __name__ == "__main__":
    rospy.init_node(node_name, anonymous=True)
    main()