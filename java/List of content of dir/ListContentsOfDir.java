/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.reno.labo;

import java.io.File;


/**
 *
 * @author re
 */
public class ListContentsOfDir {

    /**
     * List contents of a directory.
     */
    public static void listContentOfDir() {
        String mypath = "F:\\DL\\Mouh-x\\";
        File file = new File(mypath);

        String[] files = file.list();

        System.out.println("Listing contents of " + file.getPath());

        for (String f : files) {
            System.out.println(f);
        }

    }


    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        listContentOfDir();
    }

}
