// sample app called Locaty
// open the starter project in Android Studio 4.0 or later by selecting Open an existing Android Studio project from the welcome screen.


// Open LocatyService.kt and create a variable to hold the reference to SensorManager:

private lateinit var sensorManager: SensorManager

// Android Studio now prompts you to import SensorManager, so import android.hardware.SensorManager.
// Next, in onCreate, add the following code:

onCreate

// 1
sensorManager = getSystemService(SENSOR_SERVICE) as SensorManager
// 2
sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER)?.also { accelerometer ->
  sensorManager.registerListener(this, accelerometer, SensorManager.SENSOR_DELAY_NORMAL, SensorManager.SENSOR_DELAY_UI)
}
// 3
sensorManager.getDefaultSensor(Sensor.TYPE_MAGNETIC_FIELD)?.also { magneticField ->
  sensorManager.registerListener(this, magneticField, SensorManager.SENSOR_DELAY_NORMAL, SensorManager.SENSOR_DELAY_UI)
}

// After you add the code above,

import android.hardware.Sensor

// To listen to the event changes in the sensors, you need to implement the interface SensorEventListener and override its methods onAccuracyChanged and onSensorChanged.
// To do that, start by adding the following imports:

import android.hardware.SensorEvent
import android.hardware.SensorEventListener

// After that, implement SensorEventListener in LocatyService:

class LocatyService : Service(), SensorEventListener {

  override fun onAccuracyChanged(sensor: Sensor?, accuracy: Int) {
  }

  override fun onSensorChanged(event: SensorEvent?) {
  }

}


// Android system calls onSensorChanged every time there’s a new sensor event. Its SensorEvent parameter gives a set of array of size three, where each index represents a value of an axes in a coordinate
// system: event.values[0] represents x, event.values[1] represents y and event.values[2] for z.
// On the other hand, Android system only calls onAccuracyChanged when there’s a change in accuracy. SensorManager contains all the accuracy change constants in SensorManager.SENSOR_STATUS_*.
// Getting Values From the Accelerometer and Magnetometer
// In LocatyService, create the following variables:

private val accelerometerReading = FloatArray(3)
private val magnetometerReading = FloatArray(3)

// These variables will hold the latest accelerometer and magnetometer values.
// For this tutorial, you only need to use onSensorChanged since you get all the latest sensor values there. So in onSensorChanged, add the following snippet:

override fun onSensorChanged(event: SensorEvent?) {
    // 1
    if (event == null) {
        return
    }
    // 2
    if (event.sensor.type == Sensor.TYPE_ACCELEROMETER) {
        // 3
        System.arraycopy(event.values, 0, accelerometerReading, 0, accelerometerReading.size)
    } else if (event.sensor.type == Sensor.TYPE_MAGNETIC_FIELD) {
        System.arraycopy(event.values, 0, magnetometerReading, 0, magnetometerReading.size)
    }
}

// Note: A rotation matrix helps map points from the device’s coordinate system to the real-world coordinate system.
// Start by creating two arrays as follows:

private val rotationMatrix = FloatArray(9)
private val orientationAngles = FloatArray(3)

// These two arrays will hold the values of the rotation matrix and orientation angles. You’ll learn more about them soon.
// Next, create a function and name it updateOrientationAngles, then add the following code to it. Import kotlin.math.round as a rounding function.

Import kotlin.math.round

fun updateOrientationAngles() {
  // 1
  SensorManager.getRotationMatrix(rotationMatrix, null, accelerometerReading, magnetometerReading)
  // 2
  val orientation = SensorManager.getOrientation(rotationMatrix, orientationAngles)
  // 3
  val degrees = (Math.toDegrees(orientation.get(0).toDouble()) + 360.0) % 360.0
  // 4
  val angle = round(degrees * 100) / 100

}


orientation[0] = Azimuth (rotation around the -ve z-axis)
orientation[1] = Pitch (rotation around the x-axis)
orientation[2] = Roll (rotation around the y-axis)

// All these values are in radians.
// 3. Next, it converts the azimuth to degrees, adding 360 because the angle is always positive.
// 4. Finally, it rounds the angle up to two decimal places.
// Now, you need to call updateOrientationAngles inside onSensorChanged at the very end. It should look like this:


override fun onSensorChanged(event: SensorEvent?) {
  // Rest of the code

  updateOrientationAngles()
}


// Adding Direction Based on Angle
// For your next step, you need to determine which direction the user is facing. To do so, add the following code:


private fun getDirection(angle: Double): String {
   var direction = ""

   if (angle >= 350 || angle <= 10)
       direction = "N"
   if (angle < 350 && angle > 280)
       direction = "NW"
   if (angle <= 280 && angle > 260)
       direction = "W"
   if (angle <= 260 && angle > 190)
       direction = "SW"
   if (angle <= 190 && angle > 170)
       direction = "S"
   if (angle <= 170 && angle > 100)
       direction = "SE"
   if (angle <= 100 && angle > 80)
       direction = "E"
   if (angle <= 80 && angle > 10)
       direction = "NE"

   return direction
}


// Here’s what you’re doing with this code:
// You find the cardinal and intercardinal directions based on the angle you pass.
// Intercardinal directions are the intermediate directions: Northeast is 45°, southeast is 135°, southwest is 225° and northwest is 315°.
// Note: Cardinal directions are north, east, south and west. They define a clockwise rotation from north to west, with west and east being perpendicular to north and south.
// Intercardinal directions are the intermediate directions: Northeast is 45°, southeast is 135°, southwest is 225° and northwest is 315°.
// The theory behind the function above is that, according to cardinal directions, north is 0° or 360°, east is 90°, south is 180° and west is 270°.
// Next, add the code below to the end of updateOrientationAngles:


fun updateOrientationAngles() {

  val direction = getDirection(degrees)
}


// In the above variable direction, you’ll get a String for the user’s direction based on the angle that you pass.
// Now that you have the angle and direction, it’s time to pass them to MainActivity.
// Sending Data to MainActivity
// First, create a set of keys in LocatyService:

companion object {
  val KEY_ANGLE = "angle"
  val KEY_DIRECTION = "direction"
  val KEY_BACKGROUND = "background"
  val KEY_NOTIFICATION_ID = "notificationId"
  val KEY_ON_SENSOR_CHANGED_ACTION = "com.raywenderlich.android.locaty.ON_SENSOR_CHANGED"
  val KEY_NOTIFICATION_STOP_ACTION = "com.raywenderlich.android.locaty.NOTIFICATION_STOP"
}


// These are keys that you’ll use to send data from LocatyService to MainActivity.
// After that, import LocalBroadcastManager in LocatyService:

import androidx.localbroadcastmanager.content.LocalBroadcastManager

// Then add the following code in updateOrientationAngles:


fun updateOrientationAngles() {
// 1
val intent = Intent()
intent.putExtra(KEY_ANGLE, angle)
intent.putExtra(KEY_DIRECTION, direction)
intent.action = KEY_ON_SENSOR_CHANGED_ACTION
// 2
LocalBroadcastManager.getInstance(applicationContext).sendBroadcast(intent)
}

// Take a look at this code, step-by-step:
// 1. Create an intent object and put data in it with respect to its keys.
// 2. You then send out a local broadcast with the intent
// Open MainActivity and add the following code in onCreate. Also,

import LocalBroadcastManager

onCreate

LocalBroadcastManager.getInstance(this).registerReceiver(broadcastReceiver
IntentFilter(LocatyService.KEY_ON_SENSOR_CHANGED_ACTION))

// Also 

import android.content.BroadcastReceiver

// and add the following in your MainActivity.

private val broadcastReceiver: BroadcastReceiver = object : BroadcastReceiver() {
   override fun onReceive(context: Context, intent: Intent) {
     // 1
     val direction = intent.getStringExtra(LocatyService.KEY_DIRECTION)
     val angle = intent.getDoubleExtra(LocatyService.KEY_ANGLE,0.0)
     val angleWithDirection = "$angle  $direction"
     binding.directionTextView.text = angleWithDirection
     // 2
     binding.compassImageView.rotation = angle.toFloat() * -1
   }
}


// Here’s what you’re doing above:
// 1. You retrieve and assign data to views.
// 2. Since the angle you get is in a counter-clockwise direction and the views in Android rotate in a clockwise manner, you need to mirror the angle so that it becomes clockwise as well. To do this, you multiply it by -1.
// Next, paste the following code in onDestroy:

override fun onDestroy() {
  LocalBroadcastManager.getInstance(this).unregisterReceiver(broadcastReceiver)
  super.onDestroy()
}

// This will unregister your BroadcastReceiver when it’s no longer needed.
// In startForegroundServiceForSensors, add the following code:

startForegroundServiceForSensors

// 1 
val locatyIntent = Intent(this, LocatyService::class.java)
locatyIntent.putExtra(LocatyService.KEY_BACKGROUND, background)
// 2
ContextCompat.startForegroundService(this, locatyIntent)


// With this code, you’re:
// 1. Create intent for service.
// 2. Starting foreground service.
// Then, in onResume, add the following:

override fun onResume() {
  super.onResume()
  startForegroundServiceForSensors(false)
}

// As soon as your activity starts, onResume is called. You pass a false in the function because the app is in the foreground.
// Also in onPause, do the following:

override fun onPause() {
  super.onPause()
  startForegroundServiceForSensors(true)
}

onPause is called when app goes in the background. Thus, you pass true in the function to let LocatyService know that app is no longer in the foreground.

/*
// Handling Events in the Background
// When you implemented the Service, you enabled handling sensor events in the background. However, Android enforces a lot of restrictions on background processing.
// In its current implementation sensor events are handled when the app goes into the background. If, say, the system or user kills the app, no events will be processed.
// This is not ideal when using a compass. To handle this case, you need to start your service as a foreground service and show a persistent notification.
// To do so, you’ll need to add some more code to LocatyService:
//  * Keep track of when the service is backgrounded
//  * Create a notification
//  * Start the service as Foreground Service
//  * Start by opening LocatyService and adding the following variable:
*/

private var background = false

// Also, update your onStartCommand as below:

override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
  intent?.let {
     // 1
     background = it.getBooleanExtra(KEY_BACKGROUND, false)
   }
  return START_STICKY
}


// Here’s what this does:
// 1. Gets the application state from MainActivity, which you pass when you start the service.
// Next, add the following constants in LocatyService:

private val notificationActivityRequestCode = 0
private val notificationId = 1
private val notificationStopRequestCode = 2

// These are the request codes you use when creating a PendingIntent. Each PendingIntent should have a unique request code.
// To create a notification when the app is in the background, first import androidx.core.app.NotificationCompat, then add the following function:

import androidx.core.app.NotificationCompat

private fun createNotification(direction: String, angle: Double): Notification {
  // 1
  val notificationManager =
            getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager

  if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
      val notificationChannel = NotificationChannel(
                application.packageName,
                "Notifications", NotificationManager.IMPORTANCE_DEFAULT
            )

       // Configure the notification channel.
      notificationChannel.enableLights(false)
      notificationChannel.setSound(null, null)
      notificationChannel.enableVibration(false)
      notificationChannel.vibrationPattern = longArrayOf(0L)
      notificationChannel.setShowBadge(false)
      notificationManager.createNotificationChannel(notificationChannel)
  }
  
  val notificationBuilder = NotificationCompat.Builder(baseContext, application.packageName)
  // 2
  val contentIntent = PendingIntent.getActivity(
            this, notificationActivityRequestCode,
            Intent(this, MainActivity::class.java), PendingIntent.FLAG_UPDATE_CURRENT)
  // 3
  val stopNotificationIntent = Intent(this, ActionListener::class.java)
  stopNotificationIntent.action = KEY_NOTIFICATION_STOP_ACTION
  stopNotificationIntent.putExtra(KEY_NOTIFICATION_ID, notificationId)
  val pendingStopNotificationIntent =
            PendingIntent.getBroadcast(this, notificationStopRequestCode, stopNotificationIntent, PendingIntent.FLAG_UPDATE_CURRENT)

  notificationBuilder.setAutoCancel(true)
            .setDefaults(Notification.DEFAULT_ALL)
            .setContentTitle(resources.getString(R.string.app_name))
            .setContentText("You're currently facing $direction at an angle of $angle°")
            .setWhen(System.currentTimeMillis())
            .setDefaults(0)
            .setVibrate(longArrayOf(0L))
            .setSound(null)
            .setSmallIcon(R.mipmap.ic_launcher_round)
            .setContentIntent(contentIntent)
            .addAction(R.mipmap.ic_launcher_round, getString(R.string.stop_notifications), pendingStopNotificationIntent)


 return notificationBuilder.build()
}


// Here’s a breakdown of what it does:
// 1. Creates a NotificationManager.
// 2. Opens the main screen of the app on a notification tap.
// 3. Adds an intent to stop the notifications from appearing.
// Now, you’ll create a BroadcastReceiver named ActionListener.
// This will listen to broadcast for stop action when you tap the Stop Notifications button from the notification.
// Add the code block below inside LocatyService:

class ActionListener : BroadcastReceiver() {
  override fun onReceive(context: Context?, intent: Intent?) {

   if (intent != null && intent.action != null) {
       // 1
       if (intent.action.equals(KEY_NOTIFICATION_STOP_ACTION)) {
            context?.let {
               // 2
               val notificationManager =
                            context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
               val locatyIntent = Intent(context, LocatyService::class.java)
               // 3
               context.stopService(locatyIntent)
               val notificationId = intent.getIntExtra(KEY_NOTIFICATION_ID, -1)
               if (notificationId != -1) {
                  // 4
                  notificationManager.cancel(notificationId)
               }
            }
         }
      }
   }
}


// Here’s what this code does:
// 1. Checks if the broadcast’s action is same as for Stop Notifications.
// 2. Gets a reference to NotificationManager.
// 3. Stops the service.
// 4. Removes the persistent notification from the Notification Drawer.
// Now, add the ActionListener to AndroidManifest:

<receiver android:name=".LocatyService$ActionListener"/>

// Here, you register the ActionListener in AndroidManifest. You could have invoked the registeration/deregiteration during runtime also inside the class.
// When starting a foreground service, you need to register a notification if you want the service to keep running in the background.
// This applies to Android version Oreo and above.
// In onCreate of LocatyService, add the following:

onCreate of LocatyService

// 1
val notification = createNotification(getString(R.string.not_available), 0.0)
// 2
startForeground(notificationId, notification)
Here’s what this code block does:
1. Create a notification
2. Start the service with the notification as a Foreground Service
Finally, add the following snippet to the end of updateOrientationAngles:
if (background) {
   // 1
   val notification = createNotification(direction, angle)
   startForeground(notificationId, notification)
   } else {
   // 2
   stopForeground(true)
}

// ends here, by Aaqib Hussain https://www.kodeco.com/u/iaaqibhussain
// https://www.kodeco.com/10838302-sensors-tutorial-for-android-getting-started
//
