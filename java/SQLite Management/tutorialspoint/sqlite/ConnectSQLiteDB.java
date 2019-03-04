/*
 * https://www.tutorialspoint.com/sqlite/sqlite_java.htm
 */
package net.tutorialspoint.sqlite;

import java.sql.Connection;
import java.sql.DriverManager;

/**
 *
 * @author re
 */
public class ConnectSQLiteDB {

    /**
     * Connect to a SQLite database
     */
    public void connect() {
        String mypath = "Z:/Dropbox/LABO-DBX/new-myebooks/";
        String dbname = "180811.db";
        String url = "jdbc:sqlite:" + mypath + dbname;
        Connection c = null;

        try {
            Class.forName("org.sqlite.JDBC");
            c = DriverManager.getConnection(url);
        } catch (Exception e) {
            System.err.println(e.getClass().getName() + ":" + e.getMessage());
            System.exit(0);
        }
        System.out.println("Database " + dbname + " opened successfully.");
    }
}