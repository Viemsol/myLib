package com.fbloginlib;

import android.content.DialogInterface;
import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentTransaction;

import android.text.Editable;
import android.text.TextWatcher;
import android.util.Log;
import android.util.Patterns;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.FirebaseException;
import com.google.firebase.FirebaseNetworkException;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseAuthInvalidCredentialsException;
import com.google.firebase.auth.FirebaseAuthUserCollisionException;
import com.google.firebase.auth.PhoneAuthCredential;
import com.google.firebase.auth.PhoneAuthOptions;
import com.google.firebase.auth.PhoneAuthProvider;

import java.util.concurrent.TimeUnit;



/**
 * A simple {@link Fragment} subclass.
 */
public class LoginFragment extends Fragment {

    final private String TAG = "TAG_LoginFragment";

    public EditText EtEmail_temp,EtPassword_temp;
    public Button ButLogin_temp,ButPhoneVerify_temp;
    public TextView TvSignup_temp,TvForgotPw_temp;
    FirebaseAuth mFirebaseAuth;

    AlertDialog alertDialog_emailver;
    AlertDialog.Builder alertDialogBuilder_email;

    AlertDialog alertDialog_phoneVer ;
    AlertDialog.Builder  alertDialogBuilder_Phone ;

    String codeSent = "0xFF";

    // Initialize phone auth callbacks
    // [START phone_auth_callbacks]
    PhoneAuthProvider.OnVerificationStateChangedCallbacks mCallbacks;

    private void gotoMainAct()
    {

        try{
            String mainFrag = getArguments().getString("Fragment");
            Fragment f = (Fragment)(Class.forName(mainFrag).newInstance());
            FragmentManager FrManagerlogin = getActivity().getSupportFragmentManager();
            FrManagerlogin.beginTransaction().replace(((ViewGroup)getView().getParent()).getId(),f).commit();
        }catch(Exception e){
            Log.e("TAG_","level class not found",e);
        }
/*
        Log.d(TAG,"Switching to Main Fragment");
        try {
            Class<?> c = Class.forName( getActivity().getIntent().getExtras().getString("MAIN_ACTIVITY_NAME"));
            Intent intent = new Intent(getActivity(), c);
            startActivity(intent);
            intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
            getActivity().finish();
        } catch (ClassNotFoundException ignored) {
            Log.d(TAG,"Class Not found");
        }
        */

    }

    private void startPhoneNumberVerification(String phoneNumber) {
        // [START start_phone_auth]

        PhoneAuthOptions options =
                PhoneAuthOptions.newBuilder(FirebaseAuth.getInstance())
                        .setPhoneNumber(phoneNumber)       // Phone number to verify
                        .setTimeout(60L, TimeUnit.SECONDS) // Timeout and unit
                        .setActivity(getActivity())                 // Activity (for callback binding)
                        .setCallbacks(mCallbacks)          // OnVerificationStateChangedCallbacks
                        .build();
        PhoneAuthProvider.verifyPhoneNumber(options);
        Log.d(TAG,"Verification code sent ");
        // [END start_phone_auth]
        Toast.makeText(getContext(),"verification code sent to : "+phoneNumber, Toast.LENGTH_SHORT).show();
    }

    private void signInWithEmailAndPassword(String _emailid,String _password)
    {

        mFirebaseAuth.signInWithEmailAndPassword(_emailid,_password).addOnCompleteListener(getActivity(), new OnCompleteListener<AuthResult>() {
            @Override
            public void onComplete(@NonNull Task<AuthResult> task) {
                if(!task.isSuccessful())
                {
                    Log.d(TAG,"Login Fail!!");

                    try {
                        throw task.getException();
                    } catch (FirebaseAuthUserCollisionException e) {
                        // log error here
                        Log.d(TAG,""+e);

                    } catch (FirebaseNetworkException e) {
                        // log error here
                        Log.d(TAG,""+e);
                    } catch (Exception e) {
                        // log error here
                        Log.d(TAG,""+e);
                    }
                    Toast.makeText(getContext(),"Email/Password Format !", Toast.LENGTH_SHORT).show();

                }
                else
                {
                    if(mFirebaseAuth.getCurrentUser().isEmailVerified()) {
                        Log.d(TAG, "Login Successful!!");
                        gotoMainAct();

                    }
                    else
                    {
                        alertDialog_emailver.show();
                    }
                }
            }
        });
    }
    //enable SafetyNet for use with Firebase Authentication in firbase console
    //Enable Android Device Verification service
    // Set SHA256 in firbase console..
    //get SHA256 from below cli command
    //C:\Program Files\Java\jdk1.8.0_191\bin>keytool -list -v -keystore "%USERPROFILE%\.android\debug.keystore" -alias androiddebugkey -storepass android -keypass android
    private void signInWithPhoneAuthCredential(String verificationId, String code) {
        PhoneAuthCredential credential = PhoneAuthProvider.getCredential(verificationId, code);

        mFirebaseAuth.signInWithCredential(credential)
                .addOnCompleteListener(getActivity(), new OnCompleteListener<AuthResult>() {
                    @Override
                    public void onComplete(@NonNull Task<AuthResult> task) {
                        if (task.isSuccessful())
                        {
                            // Sign in success, update UI with the signed-in user's information
                            try{
                                if(!mFirebaseAuth.getCurrentUser().getDisplayName().isEmpty())
                                {
                                    Log.d(TAG, "signInWith Phone Credential:success");
                                    gotoMainAct();
                                }
                            }
                            catch (NullPointerException e) {
                                Log.d(TAG, "user not registered");
                                mFirebaseAuth.signOut();
                                Toast.makeText(getContext(),"Kindly Register", Toast.LENGTH_SHORT).show();

                            }



                            // ...
                        } else {
                            // Sign in failed, display a message and update the UI
                            Log.w(TAG, "signInWithCredential:failure", task.getException());
                            if (task.getException() instanceof FirebaseAuthInvalidCredentialsException) {
                                // The verification code entered was invalid
                                Toast.makeText(getActivity(),"verification code entered was invalid", Toast.LENGTH_SHORT).show();

                            }
                        }
                    }
                });
    }

    public LoginFragment() {
        // Required empty public constructor
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View viewLogin = inflater.inflate(R.layout.fragment_login, container, false);
        Log.d(TAG,"Created");

       // getActivity().setTitle("Login");

        if(getArguments().containsKey("OrgLogo")) {
            //set logo
            ImageView imageView = viewLogin.findViewById(R.id.imageView);
            int picture = getArguments().getInt("OrgLogo");
            imageView.setImageResource(picture);
        }

        mFirebaseAuth = FirebaseAuth.getInstance();
        EtEmail_temp = viewLogin.findViewById(R.id.EtEmail);
        EtPassword_temp = viewLogin.findViewById(R.id.EtPassword);
        ButLogin_temp = viewLogin.findViewById(R.id.ButLogin);
        ButPhoneVerify_temp =  viewLogin.findViewById(R.id.ButPhoneVerify);
        TvSignup_temp = viewLogin.findViewById(R.id.TvSignup);
        TvForgotPw_temp = viewLogin.findViewById(R.id.TvForgotPw);

        //set alert
        // create alert window
        alertDialogBuilder_email = new AlertDialog.Builder(getContext());
        alertDialogBuilder_email.setMessage("Email Not Verified !\nVerify your email by clicking link sent");
        alertDialogBuilder_email.setPositiveButton("Resend Email", new DialogInterface.OnClickListener()
        {
            @Override
            public void onClick(DialogInterface arg0, int arg1) {
                mFirebaseAuth.getCurrentUser().sendEmailVerification();

            }
        });
        alertDialogBuilder_email.setNegativeButton("Cancel",new DialogInterface.OnClickListener()
        {
            @Override
            public void onClick(DialogInterface dialog, int which)
            {
                // finish();
            }
        });

        alertDialog_emailver = alertDialogBuilder_email.create();

        // phone varification alert

        alertDialogBuilder_Phone = new AlertDialog.Builder(getContext());
        alertDialogBuilder_Phone.setMessage("Sending Code via SMS to your Phone Number.\nStandard SMS rate may be Applicable!");
        alertDialogBuilder_Phone.setPositiveButton("Send Code", new DialogInterface.OnClickListener()
        {
            @Override
            public void onClick(DialogInterface arg0, int arg1) {
                String _emailidPhone = EtEmail_temp.getText().toString();
                if(getArguments().containsKey("countryCode")) {
                    //set logo
                    _emailidPhone = getArguments().getString("countryCode")+_emailidPhone;
                }
                else
                {
                    Log.d(TAG,"Taking default country code +91");
                    _emailidPhone ="+91"+_emailidPhone;
                }
                Log.d(TAG,"Sending Verification code to :  " +_emailidPhone);

                startPhoneNumberVerification(_emailidPhone);

            }
        });
        alertDialogBuilder_Phone.setNegativeButton("Cancel",new DialogInterface.OnClickListener()
        {
            @Override
            public void onClick(DialogInterface dialog, int which)
            {
                // finish();
            }
        });

        alertDialog_phoneVer = alertDialogBuilder_Phone.create();

        EtEmail_temp.addTextChangedListener(new TextWatcher()
        {

            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count)
            {
                String _emailidPhone = EtEmail_temp.getText().toString();
                if(Patterns.PHONE.matcher(_emailidPhone).matches() && _emailidPhone.length() == 10)
                {
                    // enable varify button
                    ButPhoneVerify_temp.setVisibility(View.VISIBLE);
                    TvForgotPw_temp.setVisibility(View.GONE);
                }
                else
                {
                    // disable Phone Verify button
                    ButPhoneVerify_temp.setVisibility(View.GONE);
                    TvForgotPw_temp.setVisibility(View.VISIBLE);

                }
            }

            @Override
            public void afterTextChanged(Editable s) {


            }
        });

        //send verification code
        ButPhoneVerify_temp.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v)
            {
                alertDialog_phoneVer.show();
            }
        });
        // log in
        ButLogin_temp.setOnClickListener(new View.OnClickListener()
        {
            @Override
            public void onClick(View v) {

                String _emailidPhone = EtEmail_temp.getText().toString();
                String _password = EtPassword_temp.getText().toString();


                if(_emailidPhone.isEmpty() || _password.isEmpty())
                {
                    Toast.makeText(getContext(),"Email/phone empty!", Toast.LENGTH_SHORT).show();
                }
                else
                {
                    if(Patterns.EMAIL_ADDRESS.matcher(_emailidPhone).matches())
                    {
                        signInWithEmailAndPassword(_emailidPhone,_password);
                    }
                    else if(Patterns.PHONE.matcher(_emailidPhone).matches() && !(_password.isEmpty()))
                    {
                        signInWithPhoneAuthCredential(codeSent,_password);
                    }
                    else
                    {
                        // invalid input
                    }
                }

            }
        });

        TvSignup_temp.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {


                trasitionToSignup();

            }
        });

        TvForgotPw_temp.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                final String _emailid = EtEmail_temp.getText().toString();

                if(!(Patterns.EMAIL_ADDRESS.matcher(_emailid).matches()) )
                {
                    Toast.makeText(getContext(),"Email not valid!", Toast.LENGTH_SHORT).show();
                }
                else {

                    // Alert user and take input
                    AlertDialog.Builder alertDialogBuilder = new AlertDialog.Builder(getContext());
                    alertDialogBuilder.setMessage("Want to reset your Password ?");
                    alertDialogBuilder.setPositiveButton("Yes", new DialogInterface.OnClickListener()
                    {
                        @Override
                        public void onClick(DialogInterface arg0, int arg1) {
                            mFirebaseAuth.sendPasswordResetEmail(_emailid)
                                    .addOnCompleteListener(new OnCompleteListener<Void>() {
                                        @Override
                                        public void onComplete(@NonNull Task<Void> task) {
                                            if (task.isSuccessful()) {
                                                Toast.makeText(getContext(),"Email sent to reset Password..", Toast.LENGTH_SHORT).show();
                                            }
                                        }
                                    });

                        }
                    });
                    alertDialogBuilder.setNegativeButton("No",new DialogInterface.OnClickListener()
                    {
                        @Override
                        public void onClick(DialogInterface dialog, int which)
                        {
                            // send command
                        }
                    });
                    AlertDialog alertDialog = alertDialogBuilder.create();
                    alertDialog.show();
                }

            }
        });

        mCallbacks = new PhoneAuthProvider.OnVerificationStateChangedCallbacks() {
            @Override
            public void onVerificationCompleted(@NonNull PhoneAuthCredential phoneAuthCredential) {
                Log.d(TAG,"onVerificationCompleted" );
            }

            @Override
            public void onVerificationFailed(@NonNull FirebaseException e) {
                Log.d(TAG,"phone Varification failed" + e.toString());
            }

            @Override
            public void onCodeSent(@NonNull String s, @NonNull PhoneAuthProvider.ForceResendingToken forceResendingToken) {
                super.onCodeSent(s, forceResendingToken);
                Log.d(TAG,"Verification call back : "+s);
                codeSent = s;
            }
        };
        // [END phone_auth_callbacks]

        return viewLogin;
    }

@Override
    public void onDestroyView()
{
    super.onDestroyView();
}

private  void trasitionToSignup()
{
    // Set title bar
    Log.d(TAG,"Going to Signup");

    Bundle args = new Bundle();
    if(getArguments().containsKey("Fragment"))
    {
        String mainFrag = getArguments().getString("Fragment");
        args.putString("Fragment", mainFrag); // on sucessful login MainFragment will be swiched
    }

    if(getArguments().containsKey("OrgLogo")) {
        int testlogo1 = getArguments().getInt("OrgLogo");
        args.putInt("OrgLogo",testlogo1);
    }
    if(getArguments().containsKey("countryCode")) {
        String bagimage = getArguments().getString("countryCode");
        args.putString("countryCode",bagimage);
    }
    if(getArguments().containsKey("tcPage")) {
        String tcPage = getArguments().getString("tcPage");
        args.putString("tcPage",tcPage);
    }
    if(getArguments().containsKey("ppPage")) {
        String ppPage = getArguments().getString("ppPage");
        args.putString("ppPage",ppPage);
    }



    SignupFreg SignupActFreg = new SignupFreg();
    FragmentManager FrManager = getFragmentManager();
    SignupActFreg.setArguments(args);
    FrManager.beginTransaction().replace(((ViewGroup)getView().getParent()).getId(),SignupActFreg).commit();

}

}
