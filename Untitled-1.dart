{
  "annual_costs": [
    {
      "year": 15, // Assumes that by year 15, all 10 fleets are fully operational.
      "costs": {
        "economic_purchases": "£6 billion", // Assumes £1 billion baseline + £0.5 billion per fleet for 10 fleets. These purchases are made from UK suppliers, adhere to 100-year use standards, and include 3D printable designs for parts, which are then donated for projects.
        "build_cost": "£0.755 billion", // Assumes consistent build cost per year for ongoing construction or maintenance of ships.
        "maintenance_cost": "£2.6625 billion", // Based on maintenance for 10 fleets, including costs for maintenance workers and apprentices.
        "operational_cost": "£2.45 billion", // Operational costs for running 10 fleets, including fuel, supplies, etc.
        "staff_cost": "£57.4 million", // Cost of academic and HQ staff, assuming £50,000 per person.
        "dock_facilities_cost": "£650 million", // Initial £200 million + £50 million per additional fleet for 10 fleets.
        "academic_facilities_cost": "£400 million", // Initial setup + £20 million per year for 15 years.
        "headquarters_cost": "£100 million", // Assumes two HQs each expanded by £50 million over time.
        "overhaul_cost": "£250 million" // Assumes two fleets are undergoing major overhaul each year, costing £125 million per fleet.
      },
      "direct_employed": {
        "dock_workers": {
          "construction": 4000, // Assumes construction workers needed for ongoing projects.
          "maintenance": 220, // Sufficient for routine maintenance and overhaul of 30 vessels.
          "apprentices": 220 // One apprentice per maintenance worker for skill development and future capacity.
        },
        "crew": {
          "naval": 5490, // Based on 10 fleets, each with naval crew.
          "medical": 7200, // Medical staff for 10 hospital ships.
          "engineering": 1080, // Engineering crew for 10 engineering barges.
          "protection": 2760, // Protection crew for 10 frigates.
          "catering": 2000, // Catering staff added for all fleets.
          "it": 1000 // 100 IT staff per barge for 10 barges, supporting tech operations.
        },
        "academic_staff": {
          "trainers": {
            "naval": 135, // Assumes 25% of trainers for naval training.
            "medical": 216, // 40% for medical training due to complexity.
            "engineering": 108, // 20% for engineering training.
            "hq": 45, // 8.33% for HQ operational training.
            "catering": 36, // 6.67% for catering training.
            "it": 50, // Added trainers for IT staff, assuming 1 trainer per 20 IT staff.
            "protection": 70 // Added trainers for force protection, assuming 1 trainer per 40 protection crew.
          },
          "administrators": 125, // One administrator per 5 trainers.
          "catering": 50, // Additional catering staff at academic facilities.
          "it": 200 // IT staff for academic facilities, assuming 20 per facility for 10 facilities.
        },
        "hq_staff": {
          "planners": 150, // 30% of HQ staff for planning roles.
          "operations": 250, // 50% for operational roles.
          "administrative": 100, // 20% for administrative support.
          "catering": 25, // Catering staff for HQ operations.
          "it": 100 // IT staff for HQ, assuming 50 per HQ for two HQs.
        },
        "total_direct_employed": 23270 // Sum of all directly employed personnel across categories.
      },
      "indirect_employed": {
        "from_fleet": 34017, // Based on 1.5:1 ratio to direct employment from fleet operations.
        "from_economic_purchases": 63000, // Assumes job creation from £6 billion in economic purchases, focusing on local supply chains.
        "additional_types": {
          "manufacturing_support": 5000, // Speculative number for manufacturing jobs related to fleet operations.
          "logistics_transportation": 3000, // Jobs in logistics and transportation due to fleet needs.
          "service_industries": 2000, // Service jobs around fleet operations.
          "professional_services": 1500, // Legal, accounting, consulting jobs spurred by fleet activities.
          "hospitality_leisure": 1000, // Jobs in hospitality due to fleet personnel.
          "educational_training": 500, // Jobs from training programs related to the fleet.
          "retail_local_economy": 2000, // Retail jobs stimulated by fleet operations.
          "construction_infrastructure": 3000, // Construction jobs from fleet-related projects.
          "environmental_safety": 1000, // Jobs in environmental management and safety.
          "technology_it": 1500 // Increased to account for additional IT needs from the fleet's operations.
        },
        "total": 114517 // Sum of all indirect employment figures, adjusted for IT staff increase.
      },
      "economic_benefits": {
        "aid_delivery": "£32.5 billion", // Direct economic value from humanitarian aid delivered by the fleet, assuming high impact scenarios.
        "local_development": "£750 million", // High-end value for local economic development from projects.
        "cost_savings": "£180 million", // Savings from 3D printing, local maintenance, and efficient use of resources.
        "infrastructure_longevity": "£1.25 billion", // Value of infrastructure designed to last 100 years for 5 major projects annually.
        "soft_power": "£1 billion", // Maximum soft power impact from the fleet's operations, enhancing UK's international standing.
        "education_projects": "£250 million", // Highest value from educational impact of projects, including schools and training facilities.
        "training_of_fleet": "£300 million", // Economic value from specialized training programs for fleet personnel, enhancing operational capabilities.
        "trained_workforce": "£300 million", // Maximum economic benefit from skilled workers entering the job market, including those transitioning to civilian roles.
        "economic_purchasing": "£12 billion", // High-end multiplier effect from £6 billion in purchases, stimulating local economies.
        "indirect_employment_value": "£4.5 billion", // Assumes each indirect job adds £30,000 to GDP.
        "local_manufacturing_repair": "£200 million", // Value added from local 3D printing and repair capabilities, promoting self-sufficiency.
        "tech_spillover": "£150 million", // Economic benefits from technological innovations and education spread by fleet activities.
        "ehf_university_impact": {
          "job_creation": "£100 million", // Jobs created by the university itself, including staff and support roles.
          "public_sector_efficiency": "£50 million", // Savings and efficiency gains from graduates entering public sector roles with specialized skills.
          "innovation_transfer": "£75 million", // Value from new technologies and practices introduced by university graduates.
          "economic_multiplier": "£200 million" // Increased economic activity from the spending power of graduates and university operations, plus community projects.
        }, // ehf_university_impact is distinct from training_of_fleet and trained_workforce as it encompasses the broader economic influence of the university, including job creation, public sector efficiency, innovation transfer, and economic multipliers from its operations and alumni.
        "total_estimated_value": "£53.38 billion" // Sum of all economic benefits detailed above, providing an estimate of the fleet's total economic impact.
      },
      "year_total_cost": "£12.5716 billion" // Total cost for year 15, reflecting all expenditures including economic purchases, construction, maintenance, and staff costs.
    }
  ]
}