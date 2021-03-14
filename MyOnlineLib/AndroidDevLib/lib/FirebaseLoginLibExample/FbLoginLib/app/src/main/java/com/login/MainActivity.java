
package com.login;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentTransaction;

import android.content.DialogInterface;
import android.content.pm.ActivityInfo;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.WindowManager;

import com.fbloginlib.LoginFragment;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;

import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

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
