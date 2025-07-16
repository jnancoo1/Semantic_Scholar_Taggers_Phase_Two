import json
import re
from typing import Dict, List, Any

class ArvixSubtopicConverter:
    def __init__(self):
        # Comprehensive category-based lookup tables using Agricultural and Food Sciences classification data
        self.category_mappings = {
            # Agricultural and Food Sciences categories (afs)
            'afs': {
                'granularity': 'coarse',
                'bloom_taxonomy': 'Knowledge',
                'expertise_level': 'Intermediate',
                'base_prerequisites': ['Biology basics', 'Chemistry basics', 'Environmental science'],
                'base_next_topics': ['Sustainable agriculture', 'Food security', 'Agricultural technology', 'Rural development']
            },
            'afs.AGR': {
                'granularity': 'medium',
                'bloom_taxonomy': 'Application',
                'expertise_level': 'Intermediate',
                'base_prerequisites': ['Plant biology', 'Soil science', 'Climate science', 'Economics basics'],
                'base_next_topics': ['Precision agriculture', 'Crop management', 'Sustainable farming', 'Agricultural economics', 'Farm management']
            },
            'afs.HOR': {
                'granularity': 'fine',
                'bloom_taxonomy': 'Application',
                'expertise_level': 'Intermediate',
                'base_prerequisites': ['Plant biology', 'Soil science', 'Plant pathology', 'Botany'],
                'base_next_topics': ['Greenhouse management', 'Fruit production', 'Vegetable cultivation', 'Ornamental horticulture', 'Post-harvest technology']
            },
            'afs.ANI': {
                'granularity': 'medium',
                'bloom_taxonomy': 'Application',
                'expertise_level': 'Intermediate',
                'base_prerequisites': ['Animal biology', 'Veterinary science', 'Nutrition', 'Genetics'],
                'base_next_topics': ['Animal breeding', 'Livestock management', 'Animal welfare', 'Dairy science', 'Meat science']
            },
            'afs.FOO': {
                'granularity': 'fine',
                'bloom_taxonomy': 'Analysis',
                'expertise_level': 'Advanced',
                'base_prerequisites': ['Chemistry', 'Microbiology', 'Nutrition', 'Food safety'],
                'base_next_topics': ['Food processing', 'Food preservation', 'Food quality control', 'Nutritional science', 'Food biotechnology']
            },
            'afs.SOI': {
                'granularity': 'fine',
                'bloom_taxonomy': 'Analysis',
                'expertise_level': 'Advanced',
                'base_prerequisites': ['Chemistry', 'Geology', 'Microbiology', 'Environmental science'],
                'base_next_topics': ['Soil chemistry', 'Soil fertility management', 'Soil conservation', 'Soil microbiology', 'Pedology']
            },
            'afs.PLA': {
                'granularity': 'medium',
                'bloom_taxonomy': 'Analysis',
                'expertise_level': 'Advanced',
                'base_prerequisites': ['Botany', 'Genetics', 'Plant physiology', 'Molecular biology'],
                'base_next_topics': ['Plant breeding', 'Crop improvement', 'Plant pathology', 'Plant biotechnology', 'Seed science']
            },
            'afs.ENV': {
                'granularity': 'medium',
                'bloom_taxonomy': 'Synthesis',
                'expertise_level': 'Advanced',
                'base_prerequisites': ['Ecology', 'Environmental science', 'Systems thinking', 'Statistics'],
                'base_next_topics': ['Sustainable agriculture', 'Agroecology', 'Climate change adaptation', 'Biodiversity conservation', 'Environmental impact assessment']
            },
            'afs.ENG': {
                'granularity': 'fine',
                'bloom_taxonomy': 'Application',
                'expertise_level': 'Advanced',
                'base_prerequisites': ['Engineering fundamentals', 'Mechanical engineering', 'Electronics', 'Computer science'],
                'base_next_topics': ['Precision agriculture', 'Agricultural robotics', 'Irrigation systems', 'Farm automation', 'Agricultural machinery design']
            },
            'afs.OTHER': {
                'granularity': 'coarse',
                'bloom_taxonomy': 'Knowledge',
                'expertise_level': 'Novice',
                'base_prerequisites': ['General science', 'Agriculture basics'],
                'base_next_topics': ['Emerging topics in agricultural sciences', 'Interdisciplinary approaches', 'Agricultural policy', 'Rural sociology']
            }
        }        
        # (All non-qbio categories removed above)
        
        # Enhanced keyword-based modifiers
        self.granularity_keywords = {
            'coarse': ['review', 'survey', 'introduction', 'overview', 'general', 'broad', 'theory', 'foundations'],
            'fine': ['specific', 'detailed', 'precise', 'particular', 'exact', 'measurement', 'experimental', 'observation'],
            'medium': ['analysis', 'study', 'investigation', 'calculation', 'method', 'application', 'model']
        }
        
        self.bloom_keywords = {
            'Knowledge': ['definition', 'list', 'identify', 'describe', 'name', 'recall', 'properties', 'characteristics'],
            'Comprehension': ['explain', 'understand', 'interpret', 'summarize', 'discuss', 'mechanisms', 'processes'],
            'Application': ['apply', 'calculate', 'solve', 'implement', 'use', 'demonstrate', 'simulation', 'modeling'],
            'Analysis': ['analyze', 'examine', 'compare', 'investigate', 'determine', 'effects', 'behavior', 'dynamics'],
            'Synthesis': ['create', 'develop', 'design', 'formulate', 'construct', 'propose', 'novel', 'new'],
            'Evaluation': ['evaluate', 'assess', 'judge', 'validate', 'critique', 'test', 'performance', 'optimization']
        }
        
        self.expertise_keywords = {
            'Novice': ['basic', 'elementary', 'simple', 'introductory', 'fundamental', 'primer', 'tutorial'],
            'Intermediate': ['moderate', 'standard', 'conventional', 'typical', 'methods', 'techniques'],
            'Advanced': ['complex', 'sophisticated', 'detailed', 'comprehensive', 'advanced', 'precision'],
            'Expert': ['cutting-edge', 'novel', 'state-of-the-art', 'pioneering', 'breakthrough', 'frontier']
        }

def extract_keywords_from_text(self, text: str) -> List[str]:
        """Extract relevant agricultural and food science keywords from title and abstract."""
        text_lower = text.lower()
        keywords = []

        # Agricultural and food science domain keywords
        agri_keywords = [
            # General agriculture
            'agriculture', 'agricultural', 'farming', 'farm', 'crop', 'crops', 'cultivation', 'field',
            'harvest', 'yield', 'production', 'productivity', 'agronomy', 'agronomic', 'planting',
            'seeding', 'sowing', 'irrigation', 'fertilizer', 'pesticide', 'herbicide', 'fungicide',
            'weed', 'pest', 'disease', 'pathogen', 'integrated pest management', 'ipm', 'organic',
            'sustainable', 'precision agriculture', 'smart farming', 'mechanization', 'tillage',
            
            # Soil science
            'soil', 'soils', 'soil fertility', 'soil health', 'soil quality', 'soil chemistry',
            'soil biology', 'soil physics', 'soil erosion', 'soil conservation', 'soil management',
            'pedology', 'edaphology', 'nutrient', 'nutrients', 'nitrogen', 'phosphorus', 'potassium',
            'organic matter', 'humus', 'compost', 'mineralization', 'nitrification', 'ph', 'cation',
            'anion', 'soil texture', 'soil structure', 'porosity', 'bulk density', 'water holding',
            
            # Plant science
            'plant', 'plants', 'botany', 'plant breeding', 'plant genetics', 'plant physiology',
            'plant pathology', 'plant biology', 'seed', 'seeds', 'germination', 'seedling',
            'photosynthesis', 'transpiration', 'respiration', 'growth', 'development', 'flowering',
            'fruit', 'vegetable', 'grain', 'cereal', 'legume', 'root', 'stem', 'leaf', 'flower',
            'pollination', 'fertilization', 'gene', 'genome', 'genotype', 'phenotype', 'trait',
            'variety', 'cultivar', 'hybrid', 'mutation', 'selection', 'marker', 'qtl',
            
            # Animal science
            'livestock', 'cattle', 'dairy', 'beef', 'cow', 'bull', 'calf', 'pig', 'swine', 'pork',
            'sheep', 'lamb', 'goat', 'poultry', 'chicken', 'hen', 'rooster', 'turkey', 'duck',
            'animal', 'animals', 'animal science', 'animal husbandry', 'animal breeding',
            'animal nutrition', 'animal health', 'animal welfare', 'veterinary', 'feed', 'feeding',
            'pasture', 'grazing', 'forage', 'silage', 'hay', 'protein', 'energy', 'metabolism',
            'reproduction', 'genetics', 'milk', 'meat', 'egg', 'wool', 'fiber',
            
            # Horticulture
            'horticulture', 'horticultural', 'garden', 'gardening', 'greenhouse', 'nursery',
            'orchard', 'vineyard', 'landscape', 'landscaping', 'floriculture', 'ornamental',
            'flower', 'flowers', 'tree', 'trees', 'shrub', 'shrubs', 'turfgrass', 'lawn',
            'pruning', 'grafting', 'propagation', 'cutting', 'tissue culture', 'hydroponics',
            'aquaponics', 'urban agriculture', 'vertical farming', 'controlled environment',
            
            # Food science
            'food', 'foods', 'food science', 'food technology', 'food safety', 'food quality',
            'food processing', 'food preservation', 'nutrition', 'nutritional', 'diet', 'dietary',
            'vitamin', 'mineral', 'carbohydrate', 'fat', 'lipid', 'amino acid', 'antioxidant',
            'functional food', 'nutraceutical', 'fermentation', 'microbiology', 'pathogen',
            'spoilage', 'shelf life', 'packaging', 'storage', 'refrigeration', 'freezing',
            'dehydration', 'canning', 'pasteurization', 'sterilization', 'irradiation',
            
            # Environmental and sustainability
            'environment', 'environmental', 'sustainability', 'sustainable', 'conservation',
            'ecosystem', 'biodiversity', 'climate', 'climate change', 'greenhouse gas',
            'carbon', 'carbon footprint', 'water', 'water management', 'drought', 'flooding',
            'renewable', 'bioenergy', 'biomass', 'biofuel', 'agroecology', 'agroforestry',
            'permaculture', 'regenerative', 'circular economy', 'life cycle assessment',
            
            # Agricultural engineering
            'agricultural engineering', 'machinery', 'equipment', 'tractor', 'combine',
            'harvester', 'planter', 'cultivator', 'sprayer', 'automation', 'robotics',
            'sensor', 'gps', 'gis', 'remote sensing', 'drone', 'uav', 'internet of things',
            'iot', 'artificial intelligence', 'machine learning', 'data analytics',
            'decision support system', 'farm management software',
            
            # Research methods and techniques
            'experiment', 'experimental', 'trial', 'field trial', 'laboratory', 'analysis',
            'statistical', 'statistics', 'modeling', 'simulation', 'optimization',
            'correlation', 'regression', 'variance', 'anova', 'randomized', 'treatment',
            'control', 'replication', 'sampling', 'measurement', 'instrumentation',
            'chromatography', 'spectroscopy', 'microscopy', 'pcr', 'elisa', 'dna',
            'rna', 'protein', 'enzyme', 'metabolite', 'biomarker', 'phenotyping',
            
            # Economics and policy
            'economics', 'economic', 'cost', 'benefit', 'profit', 'income', 'market',
            'price', 'trade', 'export', 'import', 'policy', 'regulation', 'subsidy',
            'insurance', 'risk', 'management', 'supply chain', 'value chain',
            'agribusiness', 'cooperative', 'rural development', 'food security',
            'poverty', 'smallholder', 'farmer', 'producer', 'consumer'
        ]

        for keyword in agri_keywords:
            if keyword in text_lower:
                keywords.append(keyword)

        return keywords
    def determine_granularity(self, metadata: Dict[str, Any]) -> str:
            """Determine granularity level based on metadata."""
            title = metadata.get('title', '').lower()
            abstract = metadata.get('abstract', '').lower()
            text = f"{title} {abstract}"
            
            # Check for specific granularity keywords
            for level, keywords in self.granularity_keywords.items():
                if any(keyword in text for keyword in keywords):
                    return level
            
            # Default based on category
            categories = metadata.get('categories', '').split()
            primary_category = categories[0] if categories else 'afs.OTHER'
            
            return self.category_mappings.get(primary_category, {
                'granularity': 'medium',
                'bloom_taxonomy': 'Knowledge',
                'expertise_level': 'Intermediate',
                'base_prerequisites': ['Agriculture basics'],
                'base_next_topics': ['Advanced agricultural topics']
            })['granularity']

    def determine_bloom_taxonomy(self, metadata: Dict[str, Any]) -> str:
            """Determine Bloom's taxonomy level based on metadata."""
            title = metadata.get('title', '').lower()
            abstract = metadata.get('abstract', '').lower()
            text = f"{title} {abstract}"
            
            # Check for specific Bloom keywords
            for level, keywords in self.bloom_keywords.items():
                if any(keyword in text for keyword in keywords):
                    return level
            
            # Default based on category
            categories = metadata.get('categories', '').split()
            primary_category = categories[0] if categories else 'afs.OTHER'
            
            return self.category_mappings.get(primary_category, {
                'bloom_taxonomy': 'Knowledge'
            })['bloom_taxonomy']

    def determine_expertise_level(self, metadata: Dict[str, Any]) -> str:
            """Determine expertise level based on metadata."""
            title = metadata.get('title', '').lower()
            abstract = metadata.get('abstract', '').lower()
            text = f"{title} {abstract}"
            
            # Check for specific expertise keywords
            for level, keywords in self.expertise_keywords.items():
                if any(keyword in text for keyword in keywords):
                    return level
            
            # Count agricultural technical complexity indicators
            technical_indicators = [
                # Advanced agricultural techniques
                'precision agriculture', 'smart farming', 'automation', 'robotics', 'artificial intelligence',
                'machine learning', 'remote sensing', 'gis', 'gps', 'drone', 'uav', 'iot',
                'sensor', 'data analytics', 'decision support', 'optimization', 'modeling',
                'simulation', 'statistical modeling', 'regression', 'correlation', 'anova',
                
                # Advanced plant science
                'plant breeding', 'genetics', 'genomics', 'marker assisted selection', 'qtl',
                'gene expression', 'transgenic', 'crispr', 'gene editing', 'tissue culture',
                'micropropagation', 'somatic embryogenesis', 'protoplast', 'cell culture',
                'molecular biology', 'pcr', 'dna', 'rna', 'protein', 'enzyme', 'metabolite',
                
                # Advanced animal science
                'animal breeding', 'quantitative genetics', 'genomic selection', 'artificial insemination',
                'embryo transfer', 'reproductive technology', 'metabolomics', 'proteomics',
                'nutrigenomics', 'rumen microbiology', 'animal nutrition modeling',
                
                # Advanced food science
                'food chemistry', 'food microbiology', 'food biotechnology', 'functional foods',
                'nutraceuticals', 'food nanotechnology', 'encapsulation', 'bioactive compounds',
                'food safety modeling', 'hazard analysis', 'haccp', 'risk assessment',
                'shelf life prediction', 'quality assurance', 'sensory evaluation',
                
                # Advanced soil science
                'soil chemistry', 'soil physics', 'soil biology', 'soil microbiology',
                'biogeochemical cycles', 'nutrient cycling', 'soil organic matter',
                'soil enzymes', 'rhizosphere', 'mycorrhizae', 'soil-plant interactions',
                'soil carbon sequestration', 'greenhouse gas emissions',
                
                # Advanced environmental science
                'life cycle assessment', 'carbon footprint', 'water footprint',
                'environmental impact assessment', 'ecosystem services', 'agroecology',
                'climate change adaptation', 'mitigation', 'sustainability assessment',
                'biodiversity conservation', 'precision conservation',
                
                # Advanced analytical techniques
                'chromatography', 'spectroscopy', 'mass spectrometry', 'microscopy',
                'x-ray diffraction', 'nmr', 'ftir', 'hplc', 'gc-ms', 'lc-ms',
                'isotope analysis', 'elemental analysis', 'biochemical assays',
                'enzymatic assays', 'immunoassays', 'elisa', 'western blot'
            ]

            tech_count = sum(1 for term in technical_indicators if term in text)

            if tech_count >= 7:
                return 'Expert'
            elif tech_count >= 3:
                return 'Advanced'
            elif tech_count >= 1:
                return 'Intermediate'
            
            # Default based on category
            categories = metadata.get('categories', '').split()
            primary_category = categories[0] if categories else 'afs.OTHER'
            
            return self.category_mappings.get(primary_category, {
                'expertise_level': 'Intermediate'
            })['expertise_level']
   
    def generate_prerequisites(self, metadata: Dict[str, Any]) -> List[str]:
        """Generate prerequisites based on metadata."""
        prerequisites = set()
        
        # Add category-based prerequisites
        categories = metadata.get('categories', '').split()
        for category in categories:
            if category in self.category_mappings:
                prerequisites.update(self.category_mappings[category]['base_prerequisites'])
        
        # Add prerequisites based on content keywords
        title = metadata.get('title', '').lower()
        abstract = metadata.get('abstract', '').lower()
        text = f"{title} {abstract}"
        
        # Agricultural-specific prerequisites based on content
        if 'plant' in text or 'crop' in text or 'breeding' in text:
            prerequisites.add('Plant biology')
        if 'soil' in text or 'fertility' in text or 'nutrient' in text:
            prerequisites.add('Soil science')
        if 'animal' in text or 'livestock' in text or 'dairy' in text:
            prerequisites.add('Animal science')
        if 'food' in text or 'nutrition' in text or 'processing' in text:
            prerequisites.add('Food science')
        if 'environment' in text or 'sustainability' in text or 'conservation' in text:
            prerequisites.add('Environmental science')
        if 'machinery' in text or 'automation' in text or 'engineering' in text:
            prerequisites.add('Engineering fundamentals')
        if 'economics' in text or 'cost' in text or 'market' in text:
            prerequisites.add('Agricultural economics')
        if 'statistical' in text or 'analysis' in text or 'modeling' in text:
            prerequisites.add('Statistics')
        if 'genetics' in text or 'breeding' in text or 'molecular' in text:
            prerequisites.add('Genetics')
        if 'chemistry' in text or 'biochemistry' in text or 'chemical' in text:
            prerequisites.add('Chemistry')
        if 'microbiology' in text or 'pathogen' in text or 'disease' in text:
            prerequisites.add('Microbiology')
        
        return list(prerequisites) if prerequisites else ['Agriculture basics']

    def generate_next_topics(self, metadata: Dict[str, Any]) -> List[str]:
        """Generate next topics based on metadata."""
        next_topics = set()
        
        # Add category-based next topics
        categories = metadata.get('categories', '').split()
        for category in categories:
            if category in self.category_mappings:
                next_topics.update(self.category_mappings[category]['base_next_topics'])
        
        # Limit to most relevant topics
        return list(next_topics)[:6] if next_topics else ['Advanced agricultural topics']


    def generate_subtopic_name(self, metadata: Dict[str, Any]) -> str:
        """Generate a concise subtopic name from the title."""
        title = metadata.get('title', '')
        
        # Clean up the title
        title = re.sub(r'\n+', ' ', title)
        title = re.sub(r'\s+', ' ', title)
        title = title.strip()
        
        # If title is too long, try to extract the main concept
        if len(title) > 70:
            # Look for the first sentence or main clause
            sentences = re.split(r'[.:;]', title)
            if sentences and len(sentences[0].strip()) > 15:
                title = sentences[0].strip()
        
        # Final length check
        if len(title) > 80:
            title = title[:77] + "..."
        
        return title

    def convert_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Convert ArXiv metadata to educational subtopic format."""
        
        subtopic = {
            "name": self.generate_subtopic_name(metadata),
            "granularity_level": self.determine_granularity(metadata),
            "bloom_taxonomy": self.determine_bloom_taxonomy(metadata),
            "expertise_level": self.determine_expertise_level(metadata),
            "prerequisites": self.generate_prerequisites(metadata),
            "next_topics": self.generate_next_topics(metadata)
        }
        
        return subtopic

# Usage example and testing functions
def main():
    # Example ArXiv metadata
    example_metadata = {
        "id": "0704.0001",
        "submitter": "Pavel Nadolsky",
        "authors": "C. Bal\\'azs, E. L. Berger, P. M. Nadolsky, C.-P. Yuan",
        "title": "Calculation of prompt diphoton production cross sections at Tevatron and LHC energies",
        "comments": "37 pages, 15 figures; published version",
        "journal-ref": "Phys.Rev.D76:013009,2007",
        "doi": "10.1103/PhysRevD.76.013009",
        "report-no": "ANL-HEP-PR-07-12",
        "categories": "hep-ph",
        "license": None,
        "abstract": "A fully differential calculation in perturbative quantum chromodynamics is presented for the production of massive photon pairs at hadron colliders. All next-to-leading order perturbative contributions from quark-antiquark, gluon-(anti)quark, and gluon-gluon subprocesses are included, as well as all-orders resummation of initial-state gluon radiation valid at next-to-next-to-leading logarithmic accuracy. The region of phase space is specified in which the calculation is most reliable. Good agreement is demonstrated with data from the Fermilab Tevatron, and predictions are made for more detailed tests with CDF and DO data. Predictions are shown for distributions of diphoton pairs produced at the energy of the Large Hadron Collider (LHC). Distributions of the diphoton pairs from the decay of a Higgs boson are contrasted with those produced from QCD processes at the LHC, showing that enhanced sensitivity to the signal can be obtained with judicious selection of events."
    }
    
    # Additional test cases for different categories
    test_cases = [
        {
            "id": "astro-ph/0001001",
            "title": "Dark Matter Detection with Gravitational Microlensing",
            "categories": "astro-ph.CO",
            "abstract": "We present a comprehensive review of gravitational microlensing as a probe of dark matter in galaxy halos. The technique offers unique insights into the nature and distribution of compact dark objects."
        },
        {
            "id": "cond-mat/0001001", 
            "title": "Quantum Hall Effect in Graphene Bilayers",
            "categories": "cond-mat.mes-hall",
            "abstract": "We study the quantum Hall effect in bilayer graphene systems using transport measurements. The results show novel fractional quantum Hall states at specific filling factors."
        },
        {
            "id": "physics/0001001",
            "title": "Introduction to Laser Physics for Undergraduate Students",
            "categories": "physics.optics physics.ed-ph",
            "abstract": "This tutorial provides an accessible introduction to laser physics principles for undergraduate physics students. We cover basic concepts and practical applications."
        },
        {
            "id": "quant-ph/0001001",
            "title": "Quantum Error Correction Codes for Fault-Tolerant Computing",
            "categories": "quant-ph",
            "abstract": "We develop new quantum error correction codes that enable fault-tolerant quantum computation. The codes show improved performance over existing methods."
        }
    ]
    
    # Create converter instance
    converter = ArxivSubtopicConverter()
    
    print("ArXiv Metadata to Educational Subtopic Converter")
    print("=" * 60)
    print()
    
    # Test with original example
    print("EXAMPLE 1: High Energy Physics - Phenomenology")
    print("-" * 50)
    subtopic = converter.convert_metadata(example_metadata)
    print_subtopic(subtopic)
    print()
    
    # Test with additional examples
    for i, test_case in enumerate(test_cases, 2):
        category_name = get_category_description(test_case['categories'].split()[0])
        print(f"EXAMPLE {i}: {category_name}")
        print("-" * 50)
        subtopic = converter.convert_metadata(test_case)
        print_subtopic(subtopic)
        print()

def print_subtopic(subtopic):
    """Helper function to print subtopic in a formatted way."""
    print(f"Name: {subtopic['name']}")
    print(f"Granularity Level: {subtopic['granularity_level']}")
    print(f"Bloom Taxonomy: {subtopic['bloom_taxonomy']}")
    print(f"Expertise Level: {subtopic['expertise_level']}")
    print(f"Prerequisites: {', '.join(subtopic['prerequisites'])}")
    print(f"Next Topics: {', '.join(subtopic['next_topics'])}")

def get_category_description(category):
    """Get human-readable description for ArXiv categories."""
    descriptions = {
        #agricultural and food sciences
        "afs.AGR": "Agricultural Sciences",
        "afs.AFS": "Agricultural and Food Sciences",
        "afs.ANI": "Animal Sciences",
        "afs.ENV": "Environmental Sciences",
        "afs.ENG": "Engineering in Agriculture",
        "afs.FOO": "Food Sciences",
        "afs.HOR": "Horticulture",
        "afs.PLA": "Plant Sciences",
        "afs.SOI": "Soil Sciences",
        "afs.OTHER": "Other Agricultural Sciences",
    }
    return descriptions.get(category, category)

# Function to process JSON input
def process_arxiv_json(json_string: str) -> Dict[str, Any]:
    """Process ArXiv metadata from JSON string."""
    try:
        metadata = json.loads(json_string)
        converter = ArxivSubtopicConverter()
        return converter.convert_metadata(metadata)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format")
    except Exception as e:
        raise ValueError(f"Error processing metadata: {str(e)}")

# Physics category filter

# Physics and Quantitative Biology category filters
PHYSICS_CATEGORIES = {
    "astro-ph.CO", "astro-ph.EP", "astro-ph.GA", "astro-ph.HE", "astro-ph.IM", "astro-ph.SR",
    "cond-mat.dis-nn", "cond-mat.mes-hall", "cond-mat.mtrl-sci", "cond-mat.other", "cond-mat.quant-gas",
    "cond-mat.soft", "cond-mat.stat-mech", "cond-mat.str-el", "cond-mat.supr-con",
    "gr-qc", "hep-ex", "hep-lat", "hep-ph", "hep-th", "math-ph",
    "nlin.AO", "nlin.CD", "nlin.CG", "nlin.PS", "nlin.SI",
    "nucl-ex", "nucl-th",
    "physics.acc-ph", "physics.ao-ph", "physics.app-ph", "physics.atm-clus", "physics.atom-ph",
    "physics.bio-ph", "physics.chem-ph", "physics.class-ph", "physics.comp-ph", "physics.data-an",
    "physics.ed-ph", "physics.flu-dyn", "physics.gen-ph", "physics.geo-ph", "physics.hist-ph",
    "physics.ins-det", "physics.med-ph", "physics.optics", "physics.plasm-ph", "physics.pop-ph",
    "physics.soc-ph", "physics.space-ph", "quant-ph"
}
QBIO_CATEGORIES = {
    "q-bio","q-bio.BM", "q-bio.CB", "q-bio.GN", "q-bio.MN", "q-bio.NC", "q-bio.OT", "q-bio.PE", "q-bio.QM", "q-bio.SC", "q-bio.TO"
}

Agricultural_Categories = {
    "afs.AGR", "afs.AFS", "afs.ANI", "afs.ENV", "afs.ENG", "afs.FOO", "afs.HOR", "afs.PLA", "afs.SOI", "afs.OTHER"
}

def is_agriculture_paper(metadata):
    """Check if paper belongs to agricultural categories."""
    categories = metadata.get("categories", "")
    cats = set(categories.split())
    return bool(Agricultural_Categories & cats)

def is_physics_paper(metadata):
    """Check if paper belongs to physics categories."""
    categories = metadata.get("categories", "")
    cats = set(categories.split())
    return bool(PHYSICS_CATEGORIES & cats)

def is_qbio_paper(metadata):
    """Check if paper belongs to quantitative biology categories."""
    categories = metadata.get("categories", "")
    cats = set(categories.split())
    return bool(QBIO_CATEGORIES & cats)

def process_json_file(input_file: str, output_file: str = None, physics_only: bool = True, qbio_only: bool = False,agriculture_only: bool = False) -> List[Dict[str, Any]]:
    """Process ArXiv metadata from JSON file."""
    import os

    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")

    converter = ArxivSubtopicConverter()
    results = []
    physics_count = 0
    total_count = 0

    print(f"Processing file: {input_file}")
    print("=" * 50)

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            # Handle different JSON formats
            content = f.read().strip()

            # Try to parse as JSON Lines format first
            if content.startswith('{') and not content.startswith('['):
                # JSON Lines format (one JSON object per line)
                for line_num, line in enumerate(content.split('\n'), 1):
                    if line.strip():
                        try:
                            metadata = json.loads(line.strip())
                            total_count += 1


                            if physics_only and not is_physics_paper(metadata):
                                continue
                            if qbio_only and not is_qbio_paper(metadata):
                                continue
                            if agriculture_only and not is_agriculture_paper(metadata):
                                continue
                        

                            physics_count += 1
                            subtopic = converter.convert_metadata(metadata)

                            # Add original metadata for reference
                            result = {
                                'original_id': metadata.get('id', f'line_{line_num}'),
                                'original_categories': metadata.get('categories', ''),
                                'subtopic': subtopic
                            }
                            results.append(result)

                            if physics_count % 100 == 0:
                                print(f"Processed {physics_count} physics papers...")
                                # Write batch to file and clear results
                                if output_file:
                                    with open(output_file, 'a', encoding='utf-8') as f_out:
                                        for r in results:
                                            f_out.write(json.dumps(r, ensure_ascii=False) + '\n')
                                    results.clear()

                        except json.JSONDecodeError as e:
                            print(f"Warning: Invalid JSON on line {line_num}: {e}")
                            continue
            else:
                # Standard JSON format (array or single object)
                data = json.loads(content)

                # Handle single object vs array
                if isinstance(data, dict):
                    data = [data]
                elif not isinstance(data, list):
                    raise ValueError("JSON must contain an object or array of objects")

                for idx, metadata in enumerate(data, 1):
                    total_count += 1


                    if physics_only and not is_physics_paper(metadata):
                        continue
                    if qbio_only and not is_qbio_paper(metadata):
                        continue
                    if agriculture_only and not is_agriculture_paper(metadata):
                        continue

                    physics_count += 1
                    subtopic = converter.convert_metadata(metadata)

                    result = {
                        'original_id': metadata.get('id', f'item_{physics_count}'),
                        'original_categories': metadata.get('categories', ''),
                        'subtopic': subtopic
                    }
                    results.append(result)

                    if physics_count % 100 == 0:
                        print(f"Processed {physics_count} physics papers...")
                        # Write batch to file and clear results
                        if output_file:
                            with open(output_file, 'a', encoding='utf-8') as f_out:
                                for r in results:
                                    f_out.write(json.dumps(r, ensure_ascii=False) + '\n')
                            results.clear()

    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {e}")
    except Exception as e:
        raise ValueError(f"Error reading file: {e}")

    print(f"\nProcessing complete!")
    print(f"Total papers processed: {total_count}")
    print(f"Physics papers found: {physics_count}")
    print(f"Conversion success rate: {len(results)}/{physics_count}")

    # Write any remaining results
    if output_file and results:
        with open(output_file, 'a', encoding='utf-8') as f:
            for r in results:
                f.write(json.dumps(r, ensure_ascii=False) + '\n')
        print(f"Results saved to: {output_file}")
    elif not output_file:
        # Print first few results as examples
        print(f"\nFirst 3 converted subtopics:")
        print("-" * 50)
        for i, result in enumerate(results[:3]):
            print(f"\n{i+1}. ID: {result['original_id']}")
            print(f"   Categories: {result['original_categories']}")
            print_subtopic(result['subtopic'])

    return results

def show_usage():
    """Display usage information."""
    print("ArXiv Metadata to Educational Subtopic Converter")
    print("=" * 50)
    print("\nUsage:")
    print("  python converter.py <input_file> [output_file] [--all] [--qbio]")
    print("\nArguments:")
    print("  input_file   : JSON file containing ArXiv metadata")
    print("  output_file  : Optional output file for results (JSON format)")
    print("  --all        : Process all papers, not just physics papers")
    print("  --qbio       : Process only quantitative biology (q-bio) papers")
    print("\nExamples:")
    print("  python converter.py arxiv_data.json")
    print("  python converter.py arxiv_data.json results.json")
    print("  python converter.py arxiv_data.json results.json --all")
    print("\nInput file formats supported:")
    print("  - JSON array: [{...}, {...}, ...]")
    print("  - JSON Lines: {...}\\n{...}\\n...")
    print("  - Single JSON object: {...}")

# Enhanced command line interface
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        show_usage()
        sys.exit(1)
    
    if sys.argv[1] in ['-h', '--help', 'help']:
        show_usage()
        sys.exit(0)
    
    input_file = sys.argv[1]
    output_file = None
    physics_only = True
    qbio_only = False
    agriculture_only = False

    # Parse additional arguments
    if len(sys.argv) > 2:
        for arg in sys.argv[2:]:
            if arg == '--all':
                physics_only = False
                qbio_only = False
            elif arg == '--qbio':
                physics_only = False
                qbio_only = True
            elif arg == '--agri':
                physics_only = False
                qbio_only = False
                agriculture_only = True
            elif not arg.startswith('--'):
                output_file = arg

    try:
        results = process_json_file(input_file, output_file, physics_only, qbio_only, agriculture_only)

        if not output_file:
            print(f"\nUse --help for more options")
            print(f"To save results: python {sys.argv[0]} {input_file} output.json")

    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nProcessing interrupted by user")
        sys.exit(1)