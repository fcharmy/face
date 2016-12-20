1. remove android:debuggable="true" in <application> of /platforms/android/AndroidManifest.xml

2. phonegap build android

3. replace attendance-android.apk in server static folder with new one

4. update static folder of server by
	python3 manage.py collectstatic

