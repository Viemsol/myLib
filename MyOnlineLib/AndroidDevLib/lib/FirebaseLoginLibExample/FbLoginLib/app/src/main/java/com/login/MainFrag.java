package com.login;


import android.os.Bundle;

import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;

import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;


/**
 * A simple {@link Fragment} subclass.
 */
public class MainFrag extends Fragment {

    final private String TAG = "TAG_Main frag";
    public MainFrag() {
        // Required empty public constructor
    }


    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        Log.d(TAG,"Created");
        ((AppCompatActivity) getActivity()).getSupportActionBar().show();
        return inflater.inflate(R.layout.fragment_main, container, false);

    }

}
