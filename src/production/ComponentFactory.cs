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

        public ComponentFactory(WarehouseManager warehouseManager, DatabaseHelper databaseHelper)
        {
            _datebaseHelper = databaseHelper;
            _warehouseManager = warehouseManager; 
        }

        public Component CreateComponent(int typeID, int quantity, int[] allowedActivities)
        {
            string allowedActivitiesString = string.Join(",", allowedActivities);

            List<object> queryResponse = _datebaseHelper.ExecuteQuery(
                $"SELECT * FROM industryACtivityProducts WHERE productTypeID = {typeID} AND activityID IN ({allowedActivitiesString})");

            if (queryResponse.Count > 0)
            {
                return new Job(quantity, typeID, _warehouseManager, 0, 0); // TODO - Add me and te calculation
            }
            else
            {
                return new Material(quantity, typeID, _warehouseManager);
            }
        }
    }
}