# Py_Amdecoder
# - AndroidManifest.xml decoder -


Pypi URL:
https://pypi.org/project/PyAmdecoder/

install:

```sh
pip install PyAmdecoder==0.0.2
```

usage: 
```sh
from Py_Amdecoder.PyAmdecoder import PyAmdecoder 
PyAmdecoder("AndroidManifest_encode.xml")
```

output:
```sh
<?xml version="1.0" encoding="utf-8"?>
<manifest 
	xmlns:android="http://schemas.android.com/apk/res/android"
	android:versionCode="1"
	android:versionName="1.0"
	android:compileSdkVersion="30"
	android:compileSdkVersionCodename="11"
	package="com.example.myapplication"
	platformBuildVersionCode="30"
	platformBuildVersionName="11"
	>
	<uses-sdk
		android:minSdkVersion="16"
		android:targetSdkVersion="30"
		>
	</uses-sdk>
	<application
		android:theme="@7f1101bf"
		android:label="@7f10001c"
		android:icon="@7f0d0000"
		android:allowBackup="true"
		android:supportsRtl="true"
		android:roundIcon="@7f0d0001"
		android:appComponentFactory="androidx.core.app.CoreComponentFactory"
		>
		<activity
			android:theme="@7f1101c1"
			android:label="@7f10001c"
			android:name="com.example.myapplication.MainActivity"
			>
			<intent-filter
				>
				<action
					android:name="android.intent.action.MAIN"
					>
				</action>
				<category
					android:name="android.intent.category.LAUNCHER"
					>
				</category>
			</intent-filter>
		</activity>
	</application>
</manifest>
```
