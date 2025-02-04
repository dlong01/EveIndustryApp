namespace EveIndustryApp
{
    public abstract class Component
    {
        public int RequiredQuantity { get; protected set; }
        public int TypeID { get; protected set; }
        public float UnitCost { get; protected set; }

        protected WarehouseManager Storage;

        public Component(int quantity, int typeID, WarehouseManager warehouseManager)
        {
            RequiredQuantity = quantity;
            TypeID = typeID;
        }

        public abstract float GetCost();
    }

    public class Job : Component
    {
        private int _materialEfficiency = 0;
        private int _timeEfficiency = 0;
        private int _runs = 1;
        
        public Job(int quantity, int typeID, WarehouseManager warehouseManager, int me = 0, int te = 0) : base(quantity, typeID, warehouseManager)
        {
            if (me < 0 || me > 10 )
            {
                throw new ArgumentOutOfRangeException(nameof(me));
            }
            if (te < 0 || te > 20)
            {
                throw new ArgumentOutOfRangeException(nameof(te));
            }

            _materialEfficiency = me;
            _timeEfficiency = te;

            _runs = CalculateRuns();
            
        }

        private int CalculateRuns()
        {
            throw new NotImplementedException();
        }

        public override float GetCost()
        {
            throw new NotImplementedException();
        }
    }

    public class Material : Component
    {
        public Material(int quantity, int typeID, WarehouseManager warehouseManager) : base(quantity, typeID, warehouseManager) { }

        public override float GetCost()
        {
            return UnitCost * RequiredQuantity;
        }

    }
}