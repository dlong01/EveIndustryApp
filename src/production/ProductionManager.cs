namespace EveIndustryApp
{
    class ProductionManager
    {
        private WarehouseManager _warehouseManager;

        public ProductionManager(WarehouseManager warehouseManager)
        {
            _warehouseManager = warehouseManager;
        }

        public void Start()
        {
            Project test = GetProjects();
        }

        private Project GetProjects()
        {
            return new Project("Drake", 10, _warehouseManager);
        }
    }
}