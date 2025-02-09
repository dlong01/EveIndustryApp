using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using MyUtils;

namespace EveIndustryApp
{
    public class ComponentFactory
    {
        private DatabaseHelper _datebaseHelper;
        private WarehouseManager _warehouseManager;

        public ComponentFactory(WarehouseManager warehouseManager)
        {
            _datebaseHelper = new DatabaseHelper("./data/eve.db");
            _warehouseManager = warehouseManager; 
        }

        public Component CreateComponent(int typeID, int quantity, int[] allowedActivities)
        {

            if (!CheckIfMaterial(typeID, allowedActivities))
            {
                return new Job(quantity, typeID, _warehouseManager, 0, 0); // TODO - Add me and te calculation
            }
            else
            {
                return new Material(quantity, typeID, _warehouseManager);
            }
        }

        public bool CheckIfMaterial(int typeID, int[] allowedActivities)
        {

            string allowedActivitiesString = string.Join(",", allowedActivities);

            List<object> queryResponse = _datebaseHelper.ExecuteQuery(
                $"SELECT * FROM industryActivityProducts WHERE productTypeID = {typeID} AND activityID IN ({allowedActivitiesString})");
            Console.WriteLine(queryResponse.Count);
            if (queryResponse.Count > 0)
            {
                return false;
            }
            else
            {
                return true;
            }
        }
    }
}