using System;
using System.Collections.Generic;
using System.ComponentModel;
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

            ComponentFactory factory = new ComponentFactory(warehouseManager); 
           
            if (factory.CheckIfMaterial(GetTypeID(typeName), [1]))
            {
                throw new ArgumentException("No recipie found for given typeName");
            }
            else
            {
                _job = (Job)factory.CreateComponent(desiredQuantity, GetTypeID(typeName), [1]);
            }
        }

        private int GetTypeID(string typeName)
        {
            DatabaseHelper databaseHelper = new DatabaseHelper("./data/eve.db");
            List<object> typeIDQuery = databaseHelper.ExecuteQuery($"SELECT typeID FROM invTypes WHERE typeName = '{typeName}'");
            
            if (typeIDQuery.Count > 0)
            {
                string typeIDString = typeIDQuery.First().ToString();
                if (typeIDString != null)
                {
                    int typeID = int.Parse(typeIDString);
                    return typeID;
                }
            }
            throw new ArgumentException("invType not found");
        }
    }
}