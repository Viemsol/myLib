# Firebase Login Library Module (fbloginlib)
This is Firebase Login Library Module . This module can be integrated to any app to have login function.

## How to build this module 
![Building library](image/BuidLib.png)

.arr file can be found in **FbLoginLib\fbloginlib\build\outputs\fbloginlib-release.aar**

## How to Integrate this module to your APP?

- Create New Firebse project
    - Go to firebase console 
    - Create new project in firebase, give name to project 
    - Enable Email and Phone Authentication under **Authentication->Signin Methods**
    - Go to Google cloud Platform [link](https://console.cloud.google.com/apis/library/androidcheck.googleapis.com?pli=1)  
    - Click on navigation menu and select **APis & Services** and then select Dashboard .
    - Serach for **Android Device Verification** and click enable
    - Go to firebase **console -> project settings -> general -> click add fingerprint**.
        - open command.exe on Desktop PC run below CLI command to get SHA256 
        - **C:\Program Files\Java\jdk1.8.0_191\bin>keytool -list -v -keystore "%USERPROFILE%\.android\debug.keystore" -alias androiddebugkey -storepass android -keypass android**
    - Copy SHA256 and past it in fingerprint in firebase consol
- Create New Empty Project in  Android Studio
    - Add firebase db,auth and storage to Android project
    - In Android studio **Tools->Firebase->Autentication -> Email and Password-->Connect to Firebase -> Choose Existin project**
    - Select project you have just created in Firebase.
    - Now select **Add Firebase Authentication** to your App.
    - Now similarly add **runtime database** and **cloud storage**.
- Import (.aar file) fbLoginLib library to project 
    - Create lib folder in project , copy .aar file from location **(LoginApp\fbloginlib\build\outputs\aar)** and place .aar file in lib folder
    - Select **File -> New Module -> Imprt AAR ->. Select location of .aar** file from lib folder and click finish
    - Select **File -> Project structure -> Dependency -> app -> click on + icon -> Module Dependency ->Select libray we imported "fbloginlib"**
    - Add new fragment to app **File -> New -> Fragement -> fragment blank** , name it as "MainFrag" . unSelect includes and click Ok
    - Create **manu** folder under rigt click on res folder in **project -> new -> new resource directory -> change directory name to "menu" , resource type to menu -> click Ok**
    - Right click on menu folder and select **new -> select menu resouce file -> rename file it to "menu"**
    - Add blow in **activity_main.xml** under layout
    ```xml
    android:id = "@+id/activityMain"
    ```
    - Add below xml code under **menu** tag under *manu.xml*
    ```xml
     xmlns:app="http://schemas.android.com/apk/res-auto">
    <item
    android:id="@+id/mybutton"
    android:title=""
    app:showAsAction="always"
    android:icon="@drawable/logout"
    />
        <!---Icons below -->
    <!--- https://material.io/resources/icons/?style=baseline -->
    ```
    
    - Add logout logo image to **drawable** folder
    - Application Floder structure should look like below
    - ![Folder Structure](image/appFolderStruct.png)
    - Add below code in Main activity class
    ```java
    public class MainActivity extends AppCompatActivity {

    final private String TAG = "TAG_ManinAct";
    //Db
    FirebaseAuth mFirebaseAuth;
    DatabaseReference TempRef;
    private FirebaseAuth.AuthStateListener mAuthStateListener;

    //button
    @Override
    protected void  onPause()
    {
        Log.d(TAG,"Pause");
        super.onPause();
    }
    @Override
    protected void  onDestroy()
    {
        Log.d(TAG,"Destroy");
        super.onDestroy();
    }
    @Override
    protected void  onStart()
    {
        super.onStart();
        Log.d(TAG,"Starting");
        //Cross heck if not loged in
        // String UID = FirebaseAuth.getInstance().getCurrentUser().getUid();
    }

    @Override
    public  void onBackPressed()
    {
       std_onBackClick();
    }

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        Log.d(TAG,"Created");
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // set screen constrints
        std_mainActOnCreate();

        mFirebaseAuth = FirebaseAuth.getInstance();
        FirebaseUser currentUser = mFirebaseAuth.getCurrentUser();
        if ((currentUser != null))
        {
            try
            {
                if(!mFirebaseAuth.getCurrentUser().getDisplayName().isEmpty())
                {
                    Log.d(TAG, "signInWith Credential:success");
                }
            }
            catch (NullPointerException e) {
                Log.d(TAG, "user not registered");
                mFirebaseAuth.signOut();
                fbloginlib_start();
            }
            // We are Logged in
            TempRef = FirebaseDatabase.getInstance().getReference("User");
            Log.d(TAG,"Signed in sucess , setting welcome title...");
            // Name, email address etc
            String name = currentUser.getDisplayName().split("%")[0];
            String email = currentUser.getEmail();
            getSupportActionBar().setSubtitle("Welcome " + name);
            //getSupportActionBar().setTitle(getSupportActionBar().getTitle() + );

            // this is to handle logout and ..
            mAuthStateListener = new FirebaseAuth.AuthStateListener()
            {
                @Override
                public void onAuthStateChanged(@NonNull FirebaseAuth firebaseAuth) {
                    FirebaseUser mFirebaseUser = mFirebaseAuth.getCurrentUser();
                    if(mFirebaseUser == null)
                    {
                        // go back to Login
                        Log.d(TAG,"Auth state change");
                        fbloginlib_start();
                    }
                    else
                    {
                        // on chnge listener update the devices from firebase
                    }
                }
            };
            gotoMainScreen();
        }
        else {
            // lets kill main activity and pass Activity name to login activity
            fbloginlib_start();
        }
    }

    private void fbloginlib_start()
    {
        Log.d(TAG,"Switching to Login ");
        getSupportActionBar().hide();
        LoginFragment LoginActFreg = new LoginFragment();
        Bundle args = new Bundle();
        args.putString("Fragment", "com.login.MainFrag"); // on sucessful login MainFragment will be swiched
        args.putInt("OrgLogo",R.drawable.testlogo1);
        args.putString("countryCode","+91");
        args.putString("tcPage","https://google.com"); // term and condition page
        args.putString("ppPage","https://google.com"); // privacy policypage
        LoginActFreg.setArguments(args);
        loadFragment(LoginActFreg);
    }
    private void gotoMainScreen()
    {
        Log.d(TAG,"Switching to Main ");
        MainFrag MainFreg = new MainFrag();
        Bundle args = new Bundle();
        MainFreg.setArguments(args);
        loadFragment(MainFreg);
    }
    private void loadFragment(Fragment fragment)
    {
        // create a FragmentManager
        FragmentManager FrManager = getSupportFragmentManager();
        // create a FragmentTransaction to begin the transaction and replace the Fragment
        FragmentTransaction fragmentTransaction = FrManager.beginTransaction();
        // replace the FrameLayout with new Fragment
        fragmentTransaction.replace(R.id.activityMain, fragment);
        fragmentTransaction.commit(); // save the changes
    }

    // create an action bar button
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // R.menu.mymenu is a reference to an xml file named mymenu.xml which should be inside your res/menu directory.
        // If you don't have res/menu, just create a directory named "menu" inside res
        getMenuInflater().inflate(R.menu.menu, menu);
        return super.onCreateOptionsMenu(menu);
    }

    // handle button activities
    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();
        if (id == R.id.mybutton)
        {
            Fragment f = getSupportFragmentManager().findFragmentById(R.id.activityMain);

            // do something here
            // Alert user and take input
            AlertDialog.Builder alertDialogBuilder = new AlertDialog.Builder(MainActivity.this);
            if(f instanceof MainFrag)
            {
                alertDialogBuilder.setMessage(" Logging Out ?");
            }
            else
            {
                alertDialogBuilder.setMessage(" Want to exit ?");
            }

            alertDialogBuilder.setPositiveButton("Yes", new DialogInterface.OnClickListener()
            {
                @Override
                public void onClick(DialogInterface arg0, int arg1) {
                    // log out
                    FirebaseAuth.getInstance().signOut();
                    if(f instanceof MainFrag)
                    {
                        fbloginlib_start();
                    }
                    else
                    {
                        finishAffinity(); // should close the application
                    }
                }
            });
            alertDialogBuilder.setNegativeButton("No",new DialogInterface.OnClickListener()
            {
                @Override
                public void onClick(DialogInterface dialog, int which)
                {
                    // Do nothing
                }
            });

            AlertDialog alertDialog = alertDialogBuilder.create();
            alertDialog.show();
        }
        return super.onOptionsItemSelected(item);
    }

    public void std_mainActOnCreate()
    {
        // this is to avoid restart of activiry/app on orientation change
        setRequestedOrientation (ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
        //set full screen mode
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);

    }
    public void std_onBackClick()
    {
        // Alert user and take input
        AlertDialog.Builder alertDialogBuilder = new AlertDialog.Builder(this);
        alertDialogBuilder.setMessage("Want to Exit ?");
        alertDialogBuilder.setPositiveButton("Yes", new DialogInterface.OnClickListener()
        {
            @Override
            public void onClick(DialogInterface arg0, int arg1)
            {
                finishAffinity(); // should close the application
            }
        });

        alertDialogBuilder.setNegativeButton("No",new DialogInterface.OnClickListener()
        {
            @Override
            public void onClick(DialogInterface dialog, int which)
            {
                // do nothing we are on login application
            }
        });

        AlertDialog alertDialog = alertDialogBuilder.create();
        alertDialog.show();
    }
    }
    ```
    
    - now configure parameters in **fbloginlib_start()** , like contry code , logo to display, Privacy policy link , TC policy link ..etc
    - Remove text view from **activity_main.xml**
    - under app/build.gradel
    ```xml
    compileOptions {
    sourceCompatibility JavaVersion.VERSION_1_8
    targetCompatibility JavaVersion.VERSION_1_8
    }
    ```
    - Remove version field of **com.google.firebase:firebase-auth** in **app/build.gradle** as per below
    ``` code
    implementation platform('com.google.firebase:firebase-bom:26.2.0')
    implementation('com.google.firebase:firebase-auth')
    ```
    - Now build and run the tool.
    - Also Check library project **FbLoginLib** and Apllication project **FbLoginLibApp** for referace.

## How FbLoginLib library Works
- if user is not logged in, then main_activity pass control to login_fregment **login page**.
- if user is already logged in main_activity pass control to main_fregment **user page**.
- Login Screen is displayed in below cases
    - User Log out Manually
    - User Not Registered
    - User is registerd but did not login
    - User logout from server
- On sucessfull user login, login_fregment pass control to main_fregment **user page**.
- User can login using phone number or using emeail id
- User must register befor login using phone number or email id in **register page**.
- main_fregment can be used to display user specific data or tasks.

    
## How app looks like
![Folder Structure](image/appSample.png)

## Best prectice for version control
- *Your code can be open sourced, not your Keys*
    - do not push **google-services.json** to version control or git