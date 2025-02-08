using System;
using System.Drawing.Printing;

namespace EveIndustryApp
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Welcome to EveIndustryApp!");
            
            WarehouseManager warehouseManager = new WarehouseManager();
            ProductionManager productionManager = new ProductionManager(warehouseManager);

            while (true)
            {
                Console.Write("1. Jobs\n2. Warehouse\n3. Settings\n");
                var optionString = Console.ReadLine();

                if (optionString != null)
                {
                    int option;
                    if (int.TryParse(optionString, out option))
                    {
                        switch (option)
                        {
                            case 1:
                                productionManager.Start();
                                break;
                            default:
                                Console.WriteLine("Number not in range, please enter a different value");
                                break;
                        }
                    }
                    else
                    {
                        Console.WriteLine("Invalid Entry, enter a new value");
                    }
                }
            }
        }
    }
}