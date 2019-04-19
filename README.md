# robot_data_anlysis
<p align="center"><img width=100% src="https://github.com/mrl-amrl/robot_data_anlysis/blob/master/data/2019-04-18-18:35/current_manipulator.png"></p>

> **package for show feed backs analysis**

## Dependencies
`pip install matplotlib`

`pip install xlsxwriter`

## Launch

> **For run feedback analyser simply run below in CLI**
```
roslaunch mrl_robots_feedback robot_feedback_analysis.launch
```


### Launch params

---


`robot_feedback_topic`  topic that get feedback from it

`path_to_save_data        type:string`  a path to save exel and plot data

`exel_is_enable     type:bool`  enable or disable exel writer 

`plot_is_enable      type:bool`  enable or disable plot drower 

`plot_mode            type:string`


