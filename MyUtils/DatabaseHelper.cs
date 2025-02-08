using System.Data.SqlClient;
using System.Data.SQLite;
using Microsoft.VisualBasic;

namespace MyUtils
{
    public class DatabaseHelper
    {
        private string _connectionString;

        public DatabaseHelper(string dbFilePath)
        {
            _connectionString = $"Data Source={dbFilePath};Version=3;";
        }

        public List<object> ExecuteQuery(string query)
        {
            using (SQLiteConnection connection = new SQLiteConnection(_connectionString))
            {
                SQLiteCommand command = new SQLiteCommand(query, connection);
                connection.Open();
                SQLiteDataReader reader = command.ExecuteReader();
                
                return reader.Cast<object>().ToList();
            }
        }

        public void ExecuteNonQuery(string commandString)
        {
            using (SQLiteConnection connection = new SQLiteConnection(_connectionString))
            {
                SQLiteCommand command = new SQLiteCommand(commandString, connection);
                connection.Open();
                command.ExecuteNonQuery();
            }
        }
    }
}