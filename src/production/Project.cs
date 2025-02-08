using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using MyUtils;

namespace EveIndustryApp
{
    public class Project
    {
        public string TypeName;
        public int Quantity;
        public double TotalCost;

        private Job _job;

        public Project(string typeName, int desiredQuantity, WarehouseManager warehouseManager)
        {
            TypeName = typeName;
            Quantity = desiredQuantity;

            _job = new Job(Quantity, GetTypeID(typeName), warehouseManager);
        }

        private int GetTypeID(string typeName)
        {
            DatabaseHelper databaseHelper = new DatabaseHelper("./data/eve.db");
            List<object> typeIDQuery = databaseHelper.ExecuteQuery($"SELECT typeID FROM invTypes WHERE typeName = {typeName}");

            return (int)typeIDQuery.First();
        }
    }
}