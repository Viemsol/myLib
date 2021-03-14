package com.fbloginlib;


import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.net.Uri;
import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AlertDialog;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;

import android.text.Editable;
import android.text.Layout;
import android.text.TextWatcher;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.ScrollView;
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
import com.google.firebase.auth.FirebaseUser;
import com.google.firebase.auth.PhoneAuthCredential;
import com.google.firebase.auth.PhoneAuthOptions;
import com.google.firebase.auth.PhoneAuthProvider;
import com.google.firebase.auth.UserProfileChangeRequest;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

import java.util.concurrent.TimeUnit;


/**
 * A simple {@link Fragment} subclass.
 */
public class SignupFreg extends Fragment {


    final private String TAG = "TAG_SignupAct frag";

    public EditText EtEmail_temp,EtPassword_temp,EtPasswordRe_temp,EtName_temp,EtPhoneNo_Temp;
    public Button ButSignup_temp,ButPhoneVerify_temp;;
    public TextView TvSignin_temp,ppPageView_temp,tcPageView_temp;
    FirebaseAuth mFirebaseAuth;
    DatabaseReference TempRef;

    AlertDialog alertDialog_phoneVer ;

    AlertDialog.Builder  alertDialogBuilder_Phone ;

    String codeSent = "0xFF"; // just make sure some random value

    PhoneAuthProvider.OnVerificationStateChangedCallbacks mCallbacks;
    public SignupFreg() {
        // Required empty public constructor
    }


    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState)
    {

        // Inflate the layout for this fragment
        View viewSignup = inflater.inflate(R.layout.fragment_signup_freg, container, false);

        //

        Log.d(TAG,"Created");
       // getActivity().setTitle("Signup");

        if(getArguments().containsKey("OrgLogo")) {
            //set logo
            ImageView imageView = viewSignup.findViewById(R.id.imageView);
            int picture = getArguments().getInt("OrgLogo");
            imageView.setImageResource(picture);
        }
        ppPageView_temp = viewSignup.findViewById(R.id.ppPage);
        tcPageView_temp = viewSignup.findViewById(R.id.tcPage);
        if(getArguments().containsKey("ppPage")) {
            ppPageView_temp.setVisibility(View.VISIBLE);
            final String tmpUri = getArguments().getString("ppPage");
            ppPageView_temp.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {

                    Uri uri = Uri.parse(tmpUri); // missing 'http://' will cause crashed
                    Intent intent = new Intent(Intent.ACTION_VIEW, uri);
                    startActivity(intent);
                }
            });
        }

        if(getArguments().containsKey("tcPage")) {
            tcPageView_temp.setVisibility(View.VISIBLE);
            final String tmpUri = getArguments().getString("tcPage");
            tcPageView_temp.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {

                    Uri uri = Uri.parse(tmpUri); // missing 'http://' will cause crashed
                    Intent intent = new Intent(Intent.ACTION_VIEW, uri);
                    startActivity(intent);
                }
            });
        }

        if(getArguments().containsKey("tcPage")) {
            tcPageView_temp.setVisibility(View.VISIBLE);
        }

      //  getActivity().getSupportActionBar().setSubtitle("Sign Up");
        mFirebaseAuth = FirebaseAuth.getInstance();
        EtEmail_temp = viewSignup.findViewById(R.id.EtEmail);
        EtPassword_temp = viewSignup.findViewById(R.id.EtPassword);
        EtPasswordRe_temp = viewSignup.findViewById(R.id.EtPasswordRe);
        EtName_temp = viewSignup.findViewById(R.id.EtName);
        EtPhoneNo_Temp = viewSignup.findViewById(R.id.EtPhoneNo);

        ButSignup_temp = viewSignup.findViewById(R.id.ButSignup);
        ButPhoneVerify_temp =  viewSignup.findViewById(R.id.ButPhoneVerify);
        TvSignin_temp = viewSignup.findViewById(R.id.TvSignin);


        // get otp click
        // create alert window
        AlertDialog.Builder alertDialogBuilder = new AlertDialog.Builder(getContext());
        alertDialogBuilder.setMessage("Verification mail sent to your email id\nKindly Verify email and login");
        alertDialogBuilder.setPositiveButton("Ok", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface arg0, int arg1) {
               trasitionToLogin();
               // go back to login

            }
        });
        final AlertDialog alertDialog = alertDialogBuilder.create();

        EtEmail_temp.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                String _emailidPhone = EtEmail_temp.getText().toString();
                if(android.util.Patterns.PHONE.matcher(_emailidPhone).matches() && _emailidPhone.length() == 10)
                {
                    // disable
                    EtPasswordRe_temp.setVisibility(View.GONE);
                    EtPhoneNo_Temp.setVisibility(View.GONE);
                    EtPassword_temp.setHint(R.string.vcodeHint);
                    // enable varify button
                    ButPhoneVerify_temp.setVisibility(View.VISIBLE);

                }
                else
                {
                    // disable Phone Verify button
                    EtPasswordRe_temp.setVisibility(View.VISIBLE);
                    EtPhoneNo_Temp.setVisibility(View.VISIBLE);
                    EtPassword_temp.setHint(R.string.pwHint);
                    ButPhoneVerify_temp.setVisibility(View.GONE);
                }
            }

            @Override
            public void afterTextChanged(Editable s) {

            }
        });
        //send verification code
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
        ButPhoneVerify_temp.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v)
            {
                alertDialog_phoneVer.show();
            }
        });
        //signing up user
        ButSignup_temp.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                final String _emailidPhone = EtEmail_temp.getText().toString();
                final String _password = EtPassword_temp.getText().toString();
                final String _passwordRe = EtPasswordRe_temp.getText().toString();
                final String _name = EtName_temp.getText().toString();
                final String _phoneNo = EtPhoneNo_Temp.getText().toString();

                if(android.util.Patterns.PHONE.matcher(_emailidPhone).matches() && _emailidPhone.length() == 10 && !(_name.isEmpty()))
                {
                    // its phone varification
                    Log.d("TAG", "Sign in with phone no");
                    signInWithPhoneAuthCredential(codeSent,_password,_name,_emailidPhone);
                }
                else if (_emailidPhone.isEmpty() || _password.isEmpty() || _passwordRe.isEmpty() || _name.isEmpty() || _phoneNo.isEmpty() || (_phoneNo.length() < 10)  || !(_password.equals(_passwordRe))) {
                    Toast.makeText(getContext(), "Email/Password/Name/Phone/OTP format Incorrect OR empty!", Toast.LENGTH_SHORT).show();
                } else {

                    Log.d("TAG", "creating user");

                    mFirebaseAuth.createUserWithEmailAndPassword(_emailidPhone, _password).addOnCompleteListener(getActivity(), new OnCompleteListener<AuthResult>() {
                        @Override
                        public void onComplete(@NonNull Task<AuthResult> task) {
                            if (!task.isSuccessful()) {
                                Log.d(TAG, "LoginFail!!"); // nan1banyahoo.com , nandyahoo ,,,https://www.youtube.com/watch?v=4DTgE7qbD_8&list=PLgCYzUzKIBE_cyEsXgIcwC3P8ipvlSFd_&index=3
                                int error_st = 0;
                                try {
                                    throw task.getException();
                                } catch (FirebaseAuthUserCollisionException e) {
                                    // log error here
                                    error_st = 1; //user exist
                                    Log.d(TAG, "" + e);

                                } catch (FirebaseNetworkException e) {
                                    // log error here
                                    Log.d(TAG, "" + e);
                                } catch (Exception e) {
                                    // log error here
                                    Log.d(TAG, "" + e);
                                }
                                if (error_st != 0) {
                                    Toast.makeText(getContext(), "User Already Exist!", Toast.LENGTH_SHORT).show();

                                } else {
                                    Toast.makeText(getContext(), "Email/Password/Name Format !", Toast.LENGTH_SHORT).show();
                                }

                            }
                            else
                            {
                                Log.d(TAG, "User Account Created!!");
                                // create user profile
                                final FirebaseUser user_tmp = mFirebaseAuth.getCurrentUser();


                                UserProfileChangeRequest profileUpdates = new UserProfileChangeRequest.Builder()
                                        .setDisplayName(_name +"%"+_phoneNo).build();


                                user_tmp.updateProfile(profileUpdates);


                                String UID = FirebaseAuth.getInstance().getCurrentUser().getUid();
                                TempRef = FirebaseDatabase.getInstance().getReference("User");
                              /*
                                // Encode data on your side using BASE64
                                byte[] data = new byte[0];
                                try {
                                    data = _password.getBytes("UTF-8");
                                } catch (UnsupportedEncodingException e) {
                                    e.printStackTrace();
                                }
                                String base64Pw = Base64.encodeToString(data, Base64.DEFAULT);

                                // Decoding password
                                byte[] decPw = Base64.decode(base64Pw, Base64.DEFAULT);
                                String pasword = decPw.toString();
*/
                                UserProfileDb User_data = new UserProfileDb(UID, _name, _emailidPhone, "", _phoneNo);
                                TempRef.child(UID).child("UserInfo").setValue(User_data).addOnCompleteListener(new OnCompleteListener<Void>() {

                                    @Override
                                    public void onComplete(@NonNull Task<Void> task) {
                                        if (!task.isSuccessful()) {
                                            try {
                                                throw task.getException();
                                            } catch (FirebaseAuthUserCollisionException e) {
                                                // log error here
                                                Log.d(TAG, "" + e);

                                            } catch (FirebaseNetworkException e) {
                                                // log error here
                                                Log.d(TAG, "" + e);
                                            } catch (Exception e) {
                                                // log error here
                                                Log.d("TAG_err2", "" + e);
                                            }
                                            Log.d(TAG, "User write fail");
                                            Toast.makeText(getContext(), "Failed to Create User", Toast.LENGTH_SHORT).show();
                                        } else {
                                            Log.d(TAG, "Log_created Success! ");
                                            if (user_tmp.isEmailVerified()) {

                                            trasitionToLogin();
                                            } else {
                                                user_tmp.sendEmailVerification();
                                                alertDialog.show();
                                            }
                                        }
                                    }
                                });
                            }
                        }
                    });
                }
            }
        });

        TvSignin_temp.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Log.d(TAG,"Going to signin");
                trasitionToLogin(); // go back to login
            }
        });

        mCallbacks= new PhoneAuthProvider.OnVerificationStateChangedCallbacks() {
            @Override
            public void onVerificationCompleted(@NonNull PhoneAuthCredential phoneAuthCredential) {

            }

            @Override
            public void onVerificationFailed(@NonNull FirebaseException e) {

            }

            @Override
            public void onCodeSent(@NonNull String s, @NonNull PhoneAuthProvider.ForceResendingToken forceResendingToken) {
                super.onCodeSent(s, forceResendingToken);
                Log.d(TAG,"Verification call back : "+s);
                codeSent = s;
            }
        };
        // [END phone_auth_callbacks]

        return viewSignup;
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
        Toast.makeText(getContext(),"verification code sent to :"+phoneNumber, Toast.LENGTH_SHORT).show();
    }
    //enable SafetyNet for use with Firebase Authentication in firbase console
    //Enable Android Device Verification service
    // Set SHA256 in firbase console..
    //get SHA256 from below cli command
    //C:\Program Files\Java\jdk1.8.0_191\bin>keytool -list -v -keystore "%USERPROFILE%\.android\debug.keystore" -alias androiddebugkey -storepass android -keypass android
    private void signInWithPhoneAuthCredential(String verificationId, String code,final String _name,final String _emailidPhone) {
        PhoneAuthCredential credential = PhoneAuthProvider.getCredential(verificationId, code);

        mFirebaseAuth.signInWithCredential(credential)
                .addOnCompleteListener(getActivity(), new OnCompleteListener<AuthResult>() {
                    @Override
                    public void onComplete(@NonNull Task<AuthResult> task) {
                        if (task.isSuccessful())
                        {
                            Log.w(TAG, "Creating user for phone cred");
                            final FirebaseUser user_tmp = mFirebaseAuth.getCurrentUser();

                            UserProfileChangeRequest profileUpdates = new UserProfileChangeRequest.Builder()
                                    .setDisplayName(_name +"%"+_emailidPhone).build();


                            user_tmp.updateProfile(profileUpdates);

                            String UID = user_tmp.getUid();
                            TempRef = FirebaseDatabase.getInstance().getReference("User");

                            UserProfileDb User_data = new UserProfileDb(UID, _name, _emailidPhone, "", _emailidPhone);
                            TempRef.child(UID).child("UserInfo").setValue(User_data).addOnCompleteListener(new OnCompleteListener<Void>() {

                                @Override
                                public void onComplete(@NonNull Task<Void> task) {
                                    if (!task.isSuccessful()) {
                                        try {
                                            throw task.getException();
                                        } catch (FirebaseAuthUserCollisionException e) {
                                            // log error here
                                            Log.d(TAG, "" + e);

                                        } catch (FirebaseNetworkException e) {
                                            // log error here
                                            Log.d(TAG, "" + e);
                                        } catch (Exception e) {
                                            // log error here
                                            Log.d("TAG_err2", "" + e);
                                        }
                                        Log.d(TAG, "User write fail");
                                        Toast.makeText(getContext(), "Failed to Create User", Toast.LENGTH_SHORT).show();
                                    } else {
                                        Log.d(TAG, "Log_created Success! ");
                                        Log.d(TAG,"Going to signin");
                                        trasitionToLogin(); // go back to login
                                    }
                                }
                            });
                        } else {
                            // Sign in failed, display a message and update the UI
                            Log.w(TAG, "signInWithCredential:failure", task.getException());
                            if (task.getException() instanceof FirebaseAuthInvalidCredentialsException) {
                                // The verification code entered was invalid
                                Toast.makeText(getContext(),"verification code entered was invalid", Toast.LENGTH_SHORT).show();

                            }
                        }
                    }
                });
    }

    private  void trasitionToLogin()
    {
        Log.d(TAG,"Going to login");


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
        LoginFragment LoginActFreg = new LoginFragment();
        FragmentManager FrManager = getFragmentManager();
        LoginActFreg.setArguments(args);
        FrManager.beginTransaction().replace(((ViewGroup)getView().getParent()).getId(),LoginActFreg).commit();
    }

}
