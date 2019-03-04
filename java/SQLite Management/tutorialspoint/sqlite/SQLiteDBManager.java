/*
 * https://www.tutorialspoint.com/sqlite/sqlite_java.htm
 */
package net.tutorialspoint.sqlite;

import static java.lang.Integer.parseInt;
import java.sql.Connection;
import java.sql.DatabaseMetaData;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

/**
 *
 * @author re
 */
public class SQLiteDBManager {

    /**
     * Create a new database file
     *
     * @param filename the database file name
     */
    public static void createNewDatabase(String filename) {

        String mypath = "Z:/Dropbox/LABO-DBX/new-myebooks/";
        String url = "jdbc:sqlite:" + mypath + filename;

        try (Connection conn = DriverManager.getConnection(url)) {
            if (conn != null) {
                DatabaseMetaData meta = conn.getMetaData();
                System.out.println("The Driver name is " + meta.getDriverName());
                System.out.println("A new database has been created.");
            }
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }
    }

    /**
     * Connect to a SQLite database
     *
     * @return Connection object
     */
    public Connection connect() {
        String mypath = "Z:/Dropbox/LABO-DBX/new-myebooks/";
        String dbname = "180813.db";
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
        return c;
    }

    /**
     * Run CREATE, INSERT, UPDATE, DELETE queries
     *
     * @param sql SQL request
     */
    public void executeUpdateSQL(String sql) {
        Statement stmt = null;

        try {
            Connection c = this.connect();
            c.setAutoCommit(false);

            stmt = c.createStatement();
            stmt.executeUpdate(sql);

            stmt.close();
            c.commit();
            c.close();

            System.out.println("Query executed successfully.");

        } catch (SQLException e) {
            System.err.println(e.getClass().getName() + ": " + e.getMessage());
            System.exit(0);
        }
    }

    /**
     * Run SELECT query
     *
     * @param sql request
     */
    public void executeQuerySQL(String sql) {
        try {
            Statement st = null;
            Connection c = this.connect();
            c.setAutoCommit(false);

            st = c.createStatement();
            ResultSet rs = st.executeQuery(sql);

            List<String> ids = new ArrayList<>();
            List<String> names = new ArrayList<>();
            List<String> ages = new ArrayList<>();
            List<String> adrs = new ArrayList<>();
            List<String> sals = new ArrayList<>();

            System.out.println("+----+------+-----+---------+--------+");
            System.out.println("| ID | NAME | AGE | ADDRESS | SALARY |");
            System.out.println("+----+------+-----+---------+--------+");

            while (rs.next()) {
                int id = rs.getInt("id");
                String name = rs.getString("name");
                int age = rs.getInt("age");
                String address = rs.getString("address");
                float salary = rs.getFloat("salary");
                System.out.print("| ");
                System.out.print(id);
                System.out.print("  | ");
                System.out.print(name);
                System.out.print(" | ");
                System.out.print(age);
                System.out.print(" | ");
                System.out.print(address);
                System.out.print(" | ");
                System.out.print(salary);
                System.out.println();
            }
            rs.close();
            st.close();
            c.close();
            System.out.println("Operation done successfully");
        } catch (SQLException e) {
            System.err.println(e.getClass().getName() + ": " + e.getMessage());
            System.exit(0);
        }
    }

    public void testDisplay(String sql) {
        Statement stmt = null;

        try {
            Connection c = this.connect();
            c.setAutoCommit(false);

            stmt = c.createStatement();
            ResultSet rs = stmt.executeQuery(sql);
            ResultSetMetaData rsmd = rs.getMetaData();

            int columnsNumber = rsmd.getColumnCount();

            List<String> ids = new ArrayList<>();
            List<String> names = new ArrayList<>();
            List<String> ages = new ArrayList<>();
            List<String> adrs = new ArrayList<>();
            List<String> sals = new ArrayList<>();

            String[] heads = {"ID", "NAME", "AGE", "ADDRESS", "SALARY"};
            ids.add(String.valueOf(heads[0].length()));
            ids.add(heads[0]);
            names.add(String.valueOf(heads[1].length()));
            names.add(heads[1]);
            ages.add(String.valueOf(heads[2].length()));
            ages.add(heads[2]);
            adrs.add(String.valueOf(heads[3].length()));
            adrs.add(heads[3]);
            sals.add(String.valueOf(heads[4].length()));
            sals.add(heads[4]);

            while (rs.next()) {
                String id = String.valueOf(rs.getInt("id"));
                String name = rs.getString("name");
                String age = String.valueOf(rs.getInt("age"));
                String address = rs.getString("address");
                String salary = String.valueOf(rs.getFloat("salary"));

                ids.add(id);
                if (id.length() > parseInt(ids.get(0))) {
                    String set0 = ids.set(0, String.valueOf(id.length()));
                }

                names.add(name);
                if (name.length() > parseInt(names.get(0))) {
                    String set1 = names.set(0, String.valueOf(name.length()));
                }

                ages.add(age);
                if (age.length() > parseInt(ages.get(0))) {
                    String set2 = ages.set(0, String.valueOf(age.length()));
                }

                adrs.add(address);
                if (address.length() > parseInt(adrs.get(0))) {
                    String set3 = adrs.set(0, String.valueOf(address.length()));
                }

                sals.add(salary);
                if (salary.length() > parseInt(sals.get(0))) {
                    String set4 = sals.set(0, String.valueOf(salary.length()));
                }
            }

            String tmp = "+";

            int gabarit = parseInt(ids.get(0)) + 2;
            for (int i = 0; i < gabarit; i++) {
                tmp += "-";
            }
            tmp += "+";

            gabarit = parseInt(names.get(0)) + 2;
            for (int i = 0; i < gabarit; i++) {
                tmp += "-";
            }
            tmp += "+";

            gabarit = parseInt(ages.get(0)) + 2;
            for (int i = 0; i < gabarit; i++) {
                tmp += "-";
            }
            tmp += "+";

            gabarit = parseInt(adrs.get(0)) + 2;
            for (int i = 0; i < gabarit; i++) {
                tmp += "-";
            }
            tmp += "+";

            gabarit = parseInt(sals.get(0)) + 2;
            for (int i = 0; i < gabarit; i++) {
                tmp += "-";
            }
            tmp += "+\n";
            String tmp1 = tmp;

            ids = display2(ids);
            names = display2(names);
            ages = display2(ages);
            adrs = display2(adrs);
            sals = display2(sals);

            for (int k = 0; k < ids.size(); k++) {
                tmp += String.format("| %s| %s| %s| %s| %s|\n",
                        ids.get(k), names.get(k), ages.get(k), adrs.get(k), sals.get(k));
                if ((k == 0)||( k == (ids.size() - 1))) {
                    tmp += tmp1;
                }
            }

            System.out.println(tmp);

            rs.close();
            stmt.close();
            c.close();
            System.out.println("Operation done successfully.");
        } catch (SQLException e) {
            System.err.println(e.getClass().getName() + ": " + e.getMessage());
            System.exit(0);
        }
    }

    private void displayList(List list) {
        for (int j = 0; j < list.size(); j++) {
            System.out.println(list.get(j));
        }
    }

    private List<String> display2(List<String> list) {
        int gabarit = parseInt(list.get(0));
        List<String> ligne = new ArrayList<>();
        for (int i = 1; i < list.size(); i++) {
            String mot = list.get(i);
            int delta = gabarit - mot.length();

            for (int j = 0; j <= delta; j++) {
                mot += " ";
            }
            ligne.add(mot);
        }
        return ligne;
    }
}
