import androidhelper
from qsl4ahelper.fullscreenwrapper2 import *

# 菜单主界面布局定义
content = """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout
	android:layout_width="fill_parent"
	android:layout_height="fill_parent"
	android:background="#7f3faf"
	android:orientation="vertical"
	xmlns:android="http://schemas.android.com/apk/res/android">
	<ScrollView   
        android:layout_width="fill_parent"   
        android:layout_height="50dp"
        android:layout_weight="1" > 
    <!-- 标题 -->
    <TextView
	android:id="@+id/Title"
	android:layout_width="fill_parent"
	android:layout_height="wrap_content"
	android:textSize="7dp"
	android:text="Dashboard"
	android:background="#af7f3f"
	android:textColor="#ffffff"
	android:textStyle="bold"
	android:gravity="center"
	/>
    </ScrollView>
    <!-- 菜单显示 -->
    <ListView
        android:id="@+id/listview"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_weight="20"
        android:background="#7f3faf"
    />
    <!-- 退出按键 -->
    <Button
	android:layout_width="fill_parent"
	android:layout_height="50dp"
	android:text="Exit"
	android:id="@+id/but_cancle"
	android:textAllCaps="false"
	android:textSize="5dp"
	android:background="#3faf7f"
	android:textColor="#ffffff"
	android:layout_weight="1"
	android:gravity="center"/>
</LinearLayout>
"""

# 命令详情界面布局定义
poetry_app_content = """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout
	android:layout_width="fill_parent"
	android:layout_height="fill_parent"
	android:background="#7f3faf"
	android:orientation="vertical"
	xmlns:android="http://schemas.android.com/apk/res/android">
	<!-- 标题 -->
	<ScrollView   
        android:layout_width="fill_parent"   
        android:layout_height="50dp"
        android:layout_weight="1" > 
    <TextView
	android:id="@+id/Title"
	android:layout_width="fill_parent"
	android:layout_height="wrap_content"
	android:textSize="7dp"
	android:text="Dashboard"
	android:background="#af7f3f"
	android:textColor="#ffffff"
	android:textStyle="bold"
	android:gravity="center"
	/>
    </ScrollView>
    <!-- 命令执行结果显示框 -->
    <ListView
        android:id="@+id/listview"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_weight="20"
        android:background="#7f3faf"
    />
    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="vertical"
        android:layout_margin="8dp">
        
        <!-- 代码显示框 -->
        <ScrollView
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:background="#ffffff"
            android:padding="8dp"
            android:elevation="4dp">
            <TextView
                android:id="@+id/codeTextView"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:lineSpacingExtra="3dp"
                android:text=""
                android:textColor="#000000"
                android:fontFamily="monospace"
                android:gravity="start"/>
        </ScrollView>
    </LinearLayout>
	<LinearLayout
		android:layout_width="fill_parent"
		android:layout_height="50dp"
		android:orientation="horizontal"
		android:layout_weight="8">
    <!-- 执行按键 -->
	<Button
		android:layout_width="fill_parent"
		android:layout_height="50dp"
		android:text="Try"
		android:id="@+id/but_try"
		android:textAllCaps="false"
		android:background="#007f7f"
		android:textColor="#ffffffff"
		android:layout_weight="1"
		android:gravity="center"/>
    <!-- 复制按键 -->
	<Button
		android:layout_width="fill_parent"
		android:layout_height="50dp"
		android:text="Copy"
		android:id="@+id/but_copy"
		android:textAllCaps="false"
		android:background="#7f7f00"
		android:textColor="#ffffffff"
		android:layout_weight="1"
		android:gravity="center"/>
	</LinearLayout>
	<!-- 返回按键 -->
	<Button
	android:layout_width="fill_parent"
	android:layout_height="50dp"
	android:text="Back"
	android:id="@+id/but_cancle"
	android:textAllCaps="false"
	android:textSize="5dp"
	android:background="#3faf7f"
	android:textColor="#ffffff"
	android:layout_weight="1"
	android:gravity="center"/>
</LinearLayout>
"""

# 全局变量，用于记录菜单界面选中的命令
cmd_position = 0

# 菜单界面显示的命令列表
INDEX_PAGE_LIST = [
    'Location',
    'SIM State',
    'WiFi State',
    'Battery State',
    'Vibrate',
    'Microphone',
    'Camera',
    'Sensors',
    'Application Manager'
]


class GetCommandResult(object):
    """执行命令，获取对应的结果和文档"""
    def __init__(self, cmd, droid):
        self.cmd = cmd
        self.droid = droid

    def get_result(self):
        function_name = f'_get_{self.cmd}'
        if hasattr(self, function_name):
            # 判断是否包含指定命令的执行方法，已有的方法则返回执行结果
            return getattr(self, function_name)()
        return []

    def get_doc(self):
        # 判断是否包含指定命令的执行方法，已有的方法则对应代码文档
        function_name = f'_get_{self.cmd}'
        if hasattr(self, function_name):
            return getattr(self, function_name).__doc__
        return ''

    def _get_location(self):
        """droid.startLocating(1000, 5)\n""" \
            """location = droid.readLocation().result\n""" \
            """droid.stopLocating()"""
        # 启动位置服务
        self.droid.startLocating(1000, 5)
        # 获取位置信息
        location = self.droid.readLocation().result
        # 使用完后停止定位
        self.droid.stopLocating()
        if location:
            network_data = location['network']
            show_list_items = [
                f'{key}: {value}'
                for key, value in network_data.items()
            ]
            return show_list_items
        return []

    def _get_wifi_state(self):
        """wifi_info = droid.wifiGetConnectionInfo().result"""
        # 获取wifi状态数据
        wifi_info = self.droid.wifiGetConnectionInfo().result
        show_list_items = [
            f'{key}: {value}'
            for key, value in wifi_info.items()
        ]  # 将获取到的所有结果显示到页面上
        return show_list_items

    def _get_sim_state(self):
        """sim_state = droid.getSimState().result\n""" \
            """network_operator = droid.getNetworkOperator().result\n""" \
            """network_operator_name = droid.getNetworkOperatorName().result"""
        show_list_items = [
            f'State: {self.droid.getSimState().result}',  # 获取SIM卡信息
            f'NetworkOperator: {self.droid.getNetworkOperator().result}',  # 返回当前注册运营商的数字名称 (MCC+MNC)
            f'NetworkOperatorName: {self.droid.getNetworkOperatorName().result}',  # 返回当前注册运营商的名称
        ]
        return show_list_items

    def _get_battery_state(self):
        """battery_status = droid.batteryGetStatus().result\n""" \
            """battery_level = droid.batteryGetLevel().result\n""" \
            """battery_temperature = droid.batteryGetTemperature().result\n"""
        show_list_items = [
            f'Battery Status: {self.droid.batteryGetStatus().result}',  # 获取电池状态
            f'Battery Level: {self.droid.batteryGetLevel().result}',  # 获取电池电量
            f'Battery Temperature: {self.droid.batteryGetTemperature().result}',  # 获取电池温度
        ]
        return show_list_items

    def _get_vibrate(self):
        """droid.vibrate(300)"""
        self.droid.vibrate(300)  # 振动300毫秒
        return ['Vibrate(300)']

    def _get_microphone(self):
        """droid.ttsSpeak("Start recording")\n"""\
            """result = droid.recorderStartMicrophone()\n"""\
            """time.sleep(5)\n"""\
            """droid.ttsSpeak("End of recording")\n"""\
            """droid.recorderStop()\n"""\
            """recording_result = result.result\n"""\
            """droid.mediaPlay(recording_result)"""
        self.droid.ttsSpeak("Start recording")
        # 开始录音
        result = self.droid.recorderStartMicrophone()
        # 等待录音5秒
        time.sleep(5)
        self.droid.ttsSpeak("End of recording")
        # 结束录音
        self.droid.recorderStop()
        # 获取录音结果
        recording_result = result.result
        # 播放录音文件
        self.droid.mediaPlay(recording_result)
        return [f'Voice: {recording_result}']

    def _get_camera(self):
        """droid.cameraCapturePicture().result"""
        # 打开相机拍照
        result = self.droid.cameraCapturePicture().result
        return [f'Picture: {result}']

    def _get_sensors(self):
        """droid.startSensingTimed(4, 1000)"""
        # 开启传感器
        self.droid.startSensingTimed(4, 1000)
        # 读取传感器结果
        result = self.droid.readSensors().result
        # 关闭传感器
        self.droid.stopSensing()
        return [f'{key}: {value}'
                for key, value in result.items()]

    def _get_application_manager(self):
        """running_app = droid.getRunningPackages().result\n"""\
            """launchable_packages = droid.getLaunchablePackages().result"""
        # 获取正在运行的应用
        running_app = self.droid.getRunningPackages().result
        # 获取所有可启动应用程序类名的列表
        launchable_packages = self.droid.getLaunchablePackages().result
        launchable_packages = '\n' + '\n'.join([f'{key}: {val}' for key, val in launchable_packages.items()])
        return [f'Running Packages: {";".join(running_app)}',
                f'Launchable Packages: {launchable_packages}']


class MainScreen(Layout):
    def __init__(self):
        super(MainScreen, self).__init__(content, "IndexApp")

    def on_show(self):
        list_view = self.views.listview
        # 将菜单列表设置到主界面
        list_view.set_listitems(INDEX_PAGE_LIST)
        # 为菜单项添加点击事件
        list_view.add_event(itemclick_EventHandler(list_view, self.cmd_details))
        # 为退出件添加事件
        self.views.but_cancle.add_event(click_EventHandler(self.views.but_cancle, self.exit))

    def cmd_details(self, view, event):
        global cmd_position
        # 获取用户点击的菜单项位置
        cmd_position = event['data']['position']
        # 关闭当前界面
        FullScreenWrapper2App.close_layout()

    def on_close(self):
        pass

    def exit(self, view, dummy):
        droid = FullScreenWrapper2App.get_android_instance()
        droid.makeToast("Exit")
        # 关闭界面
        FullScreenWrapper2App.close_layout()
        global cmd_position
        # 设置全局变量
        cmd_position = -1


class CommandDetails(Layout):
    def __init__(self):
        super(CommandDetails, self).__init__(poetry_app_content, "DetailsApp")

    def on_show(self):
        list_view = self.views.listview
        droid = FullScreenWrapper2App.get_android_instance()
        position = int(cmd_position)
        title = 'Details'
        try:
            # 根据全局变量cmd_position获取对应的命令
            title = INDEX_PAGE_LIST[position]
            cmd = title.lower().replace(' ', '_')
            cmd_res = GetCommandResult(cmd, droid)
            # 获取命令对应的执行结果
            show_list_items = cmd_res.get_result()
            # 获取命令对应的文档
            code = cmd_res.get_doc()
            # 将代码设置到界面的代码显示框中
            self.views.codeTextView.text = code
        except Exception as e:
            show_list_items = [f'ServerError: {str(e)}']
        # 将命令执行结果设置到页面
        list_view.set_listitems(show_list_items)
        # 将命令设置为页面标题
        self.views.Title.text = title
        # 为复制按键添加事件
        self.views.but_copy.add_event(click_EventHandler(self.views.but_copy, self.copy_code))
        # 为返回按键添加事件
        self.views.but_cancle.add_event(click_EventHandler(self.views.but_cancle, self.back))
        # 为执行按键添加事件
        self.views.but_try.add_event(click_EventHandler(self.views.but_try, self.retry))

    def on_close(self):
        pass

    def back(self, view, dummy):
        # 关闭当前页面
        FullScreenWrapper2App.close_layout()

    def copy_code(self, view, dummy):
        droid = FullScreenWrapper2App.get_android_instance()
        # 将代码框中的文本设置到剪贴板
        droid.setClipboard(self.views.codeTextView.text)
        droid.makeToast("Copied")

    def retry(self, view, dummy):
        # 执行命令，显示结果
        list_view = self.views.listview
        droid = FullScreenWrapper2App.get_android_instance()
        position = int(cmd_position)
        try:
            title = INDEX_PAGE_LIST[position]
            cmd = title.lower().replace(' ', '_')
            cmd_res = GetCommandResult(cmd, droid)
            show_list_items = cmd_res.get_result()
            code = cmd_res.get_doc()
            self.views.codeTextView.text = code
        except Exception as e:
            show_list_items = [f'ServerError: {str(e)}']
        list_view.set_listitems(show_list_items)


def index_page():
    # 运行主界面
    droid = androidhelper.Android()
    FullScreenWrapper2App.initialize(droid)
    FullScreenWrapper2App.show_layout(MainScreen())
    FullScreenWrapper2App.eventloop()
    return cmd_position


def detail_page():
    # 运行命令详情页面
    droid = androidhelper.Android()
    FullScreenWrapper2App.initialize(droid)
    FullScreenWrapper2App.show_layout(CommandDetails())
    FullScreenWrapper2App.eventloop()


if __name__ == '__main__':
    while True:
        position = index_page()
        if position == -1:  # 退出应用
            break
        detail_page()
