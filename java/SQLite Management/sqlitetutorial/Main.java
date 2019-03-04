/*
 * http://www.sqlitetutorial.net/sqlite-java/
 */
package net.sqlitetutorial;

/**
 *
 * @author re
 */
public class Main {

    /**
     * @param args the CLI arguments
     */
    public static void main(String[] args) {

        //SQLiteDBManager obj = new SQLiteDBManager();
        String dbpath = "Z:/Dropbox/LABO-DBX/new-myebooks/";
        String dbname = "180811.db";
        String url = "jdbc:sqlite:" + dbpath + dbname;

        BLOBApp app = new BLOBApp();
        app.updatePicture(1, "Z:\\Temp\\hp_laptop.jpg");

        // read blob and write data into a file
        app.readPicture(1, "Z:\\Temp\\laptop.jpg");

    }
}
