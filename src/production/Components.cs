using MyUtils;

namespace EveIndustryApp
{
    public abstract class Component
    {
        public int RequiredQuantity { get; protected set; }
        public int TypeID { get; protected set; }
        public double UnitCost { get; protected set; }

        protected DatabaseHelper _databaseHelper;
        protected WarehouseManager _warehouseManager;
        protected int _quantityToAquire; 

        public Component(int quantity, int typeID, WarehouseManager warehouseManager)
        {
            RequiredQuantity = quantity;
            TypeID = typeID;

            _warehouseManager = warehouseManager;
            CalculateQuantityToAquire();

            _databaseHelper = new DatabaseHelper(".data/eve.db");
        }

        private void CalculateQuantityToAquire()
        {
            // TODO - Workout how many of each item are stored in the warehouse and therefore how many will need to be produced/bought
            _quantityToAquire = RequiredQuantity; 
        }
        public abstract double GetCost();
    }

    public class Job : Component
    {
        public int SpareProduced;
        private int _materialEfficiency = 0;
        private int _timeEfficiency = 0;
        private int _runs = 1;
        private int _activityID = 1;

        private List<Component> _components = new List<Component>();
        
        public Job(int quantity, int typeID, WarehouseManager warehouseManager, int me = 0, int te = 0)
            : base(quantity, typeID, warehouseManager)
        {
            if (me < 0 || me > 10)
            {
                throw new ArgumentOutOfRangeException(nameof(me));
            }
            if (te < 0 || te > 20)
            {
                throw new ArgumentOutOfRangeException(nameof(te));
            }

            _materialEfficiency = me;
            _timeEfficiency = te;

            CalculateRuns();
            CalculateComponents();
        }

        private void CalculateRuns()
        {
            string query = $"SELECT quantity FROM industryActivityProducts WHERE typeID = {TypeID}, activityID = {_activityID}";

            int quantityPerRun = (int)_databaseHelper.ExecuteQuery(query).First();

            _runs = (int)Math.Ceiling(_quantityToAquire / (double)quantityPerRun);
            SpareProduced = (_runs * quantityPerRun) - _quantityToAquire;
        }

        private void CalculateComponents()
        {
            string query = $"SELECT typeID FROM industryActivityProducts WHERE productTypeID = {TypeID}, activityID = {_activityID}";
            int activityTypeID = (int)_databaseHelper.ExecuteQuery(query).First();

            query = $"SELECT materialTypeID, quantity FROM industryActivityMaterials WHERE typeID = {activityTypeID}, activityID = {_activityID}";
            List<int[]> components = _databaseHelper.ExecuteQuery(query).Cast<int[]>().ToList();

            ComponentFactory componentFactory = new ComponentFactory(_warehouseManager, _databaseHelper);
            foreach (int[] componentInfo in components)
            {
                _components.Add(componentFactory.CreateComponent(componentInfo[0], ComponentQuantityNeeded(componentInfo[1]), [_activityID]));
            }
        }

        private int ComponentQuantityNeeded(int requiredPerRun)
        {
            int quantityNeeded = _runs * requiredPerRun;
            quantityNeeded = (int)Math.Ceiling((double)(quantityNeeded * ((100 - _materialEfficiency) / 100)));

            if (quantityNeeded < _runs) { quantityNeeded = _runs; }

            return quantityNeeded;
        }

        public override double GetCost()
        {
            throw new NotImplementedException();
        }
    }

    public class Material : Component
    {
        public Material(int quantity, int typeID, WarehouseManager warehouseManager)
            : base(quantity, typeID, warehouseManager) { }

        public override double GetCost()
        {
            return UnitCost * RequiredQuantity;
        }
    }
}