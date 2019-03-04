/*
 * https://www.tutorialspoint.com/sqlite/sqlite_java.htm
 */
package net.tutorialspoint.sqlite;

/**
 *
 * @author re
 */
public class Main {

    public static void main(String[] args) {
        SQLiteDBManager session = new SQLiteDBManager();

        //session.createNewDatabase("180813.db");

        // Insert
        /*sql = "INSERT INTO company (id, name, age, address, salary) VALUES"
                + "(1, 'Paul', 32, 'Cali'),"
                + "(2, 'Allen', 25, 'Texas', 15000.00 ),"
                + "(3, 'Teddy', 23, 'Norway', 20000.00 ),"
                + "(4, 'Mark', 25, 'Rich-Mond ', 65000.00 );";
         */
        String sql_createTable = "CREATE TABLE IF NOT EXISTS COMPANY "
                + "(id INT PRIMARY KEY     NOT NULL,"
                + " name           TEXT    NOT NULL, "
                + " age            INT     NOT NULL, "
                + " address        CHAR(50), "
                + " salary         REAL);";
        String sql_insert = "INSERT INTO company (id, name, age, address, salary) VALUES"
                + "(1, 'Paul', 32, 'California', 20000.00),"
                + "(2, 'Allen', 25, 'Texas', 15000.00 ),"
                + "(3, 'Teddy', 23, 'Norway', 20000.00 ),"
                + "(4, 'Mark', 25, 'Rich-Mond ', 65000.00 );";
        String sql_select = "SELECT * FROM COMPANY;";

        session.executeUpdateSQL("DELETE FROM COMPANY;");
        session.executeUpdateSQL(sql_insert);
        session.testDisplay(sql_select);
        //session.executeQuerySQL("SELECT * FROM COMPANY;");
        //session.executeUpdateSQL("UPDATE COMPANY set SALARY = 95000.00 where ID=1;");
        //session.executeUpdateSQL("DELETE from COMPANY where ID=2;");
    }
}
