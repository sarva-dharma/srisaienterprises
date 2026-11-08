import json
import sys

schema_data = {
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": ["LocalBusiness", "Store", "ProfessionalService"],
      "@id": "https://sarva-dharma.github.io/srisaienterprises/#store",
      "name": "Sri Sai Enterprises",
      "alternateName": [
        "ಶ್ರೀ ಸಾಯಿ ಎಂಟರ್ ಪ್ರೈಸಸ್",
        "ಶ್ರೀ ಸಾಯಿ ಎಂಟರ್‌ಪ್ರೈಸಸ್",
        "Sri Sai Enterprises Bengaluru",
        "Sri Sai Enterprises Since 1989"
      ],
      "legalName": "Sri Sai Enterprises",
      "url": "https://sarva-dharma.github.io/srisaienterprises/",
      "logo": {
        "@type": "ImageObject",
        "url": "https://sarva-dharma.github.io/srisaienterprises/static/images/bbmp_official_logo.jpg",
        "width": "400",
        "height": "400"
      },
      "image": [
        "https://sarva-dharma.github.io/srisaienterprises/static/images/bbmp_tower_web.jpg",
        "https://sarva-dharma.github.io/srisaienterprises/static/images/bbmp_headquarters.jpg"
      ],
      "description": "Sri Sai Enterprises (Since 1989) is Bengaluru's premier architectural and municipal building plan approval practice, delivering 23,000+ sanctions across GBA, BBMP, BDA, and BIAAPA.",
      "foundingDate": "1989",
      "telephone": "+91-9448054185",
      "email": "smthyagaraj@gmail.com",
      "priceRange": "₹₹",
      "currenciesAccepted": "INR",
      "paymentAccepted": "Cash, UPI, Credit Card, Debit Card, Net Banking, Cheque",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "#3309, 1st Main Road, Gayathrinagar",
        "addressLocality": "Bengaluru",
        "addressRegion": "Karnataka",
        "postalCode": "560021",
        "addressCountry": "IN"
      },
      "geo": {
        "@type": "GeoCoordinates",
        "latitude": 12.9965,
        "longitude": 77.5562
      },
      "hasMap": "https://maps.google.com/?q=Gayathrinagar+Bangalore",
      "openingHoursSpecification": [
        {
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday"
          ],
          "opens": "09:30",
          "closes": "19:30"
        }
      ],
      "areaServed": [
        {
          "@type": "City",
          "name": "Bengaluru",
          "sameAs": "https://en.wikipedia.org/wiki/Bangalore"
        },
        {
          "@type": "AdministrativeArea",
          "name": "Bangalore Urban",
          "sameAs": "https://en.wikipedia.org/wiki/Bangalore_Urban_district"
        },
        {
          "@type": "AdministrativeArea",
          "name": "Greater Bengaluru Authority (GBA)"
        },
        {
          "@type": "AdministrativeArea",
          "name": "Bruhat Bengaluru Mahanagara Palike (BBMP)"
        },
        {
          "@type": "AdministrativeArea",
          "name": "Bangalore Development Authority (BDA)"
        },
        {
          "@type": "AdministrativeArea",
          "name": "BIAAPA"
        },
        {
          "@type": "AdministrativeArea",
          "name": "BMRDA"
        },
        {
          "@type": "AdministrativeArea",
          "name": "STRR"
        }
      ],
      "founder": {
        "@type": "Person",
        "@id": "https://sarva-dharma.github.io/srisaienterprises/#founder",
        "name": "S. M. Thyagaraja",
        "alternateName": "ಎಸ್. ಎಂ. ತ್ಯಾಗರಾಜ",
        "jobTitle": "Principal Architect & Draftsman Civil",
        "telephone": "+91-9448054185",
        "hasCredential": [
          {
            "@type": "EducationalOccupationalCredential",
            "credentialCategory": "Professional License",
            "name": "Council of Architecture Registration",
            "recognizedBy": {
              "@type": "Organization",
              "name": "Council of Architecture (India)"
            },
            "identifier": "CA/2009/44120"
          },
          {
            "@type": "EducationalOccupationalCredential",
            "credentialCategory": "Municipal Supervisor License",
            "name": "BBMP Approved Technical Supervisor License",
            "recognizedBy": {
              "@type": "GovernmentOrganization",
              "name": "Bruhat Bengaluru Mahanagara Palike"
            },
            "identifier": "BCC/BL-3.2.3/S-218/89-90"
          }
        ]
      },
      "sameAs": [
        "https://bpas.bbmpgov.in",
        "https://wa.me/919448054185"
      ]
    },
    {
      "@type": "WebSite",
      "@id": "https://sarva-dharma.github.io/srisaienterprises/#website",
      "url": "https://sarva-dharma.github.io/srisaienterprises/",
      "name": "Sri Sai Enterprises",
      "alternateName": "ಶ್ರೀ ಸಾಯಿ ಎಂಟರ್ ಪ್ರೈಸಸ್",
      "description": "Official Web Platform for Sri Sai Enterprises - Building Plan Approvals, Architecture, Estimation & Land Surveying in Bengaluru since 1989.",
      "publisher": {
        "@id": "https://sarva-dharma.github.io/srisaienterprises/#store"
      },
      "inLanguage": ["en-IN", "kn-IN"],
      "potentialAction": {
        "@type": "SearchAction",
        "target": {
          "@type": "EntryPoint",
          "urlTemplate": "https://sarva-dharma.github.io/srisaienterprises/?q={search_term_string}#jurisdiction-checker"
        },
        "query-input": "required name=search_term_string"
      }
    },
    {
      "@type": "BreadcrumbList",
      "@id": "https://sarva-dharma.github.io/srisaienterprises/#breadcrumb",
      "itemListElement": [
        {
          "@type": "ListItem",
          "position": 1,
          "name": "Home (ಮುಖಪುಟ)",
          "item": "https://sarva-dharma.github.io/srisaienterprises/"
        },
        {
          "@type": "ListItem",
          "position": 2,
          "name": "Services (ಸೇವೆಗಳು)",
          "item": "https://sarva-dharma.github.io/srisaienterprises/#services"
        },
        {
          "@type": "ListItem",
          "position": 3,
          "name": "Jurisdiction & Zoning (ವಲಯ ಪರಿಶೀಲನೆ)",
          "item": "https://sarva-dharma.github.io/srisaienterprises/#jurisdiction-checker"
        },
        {
          "@type": "ListItem",
          "position": 4,
          "name": "Cost Estimator (ವೆಚ್ಚ ಅಂದಾಜು)",
          "item": "https://sarva-dharma.github.io/srisaienterprises/#fee-estimator"
        },
        {
          "@type": "ListItem",
          "position": 5,
          "name": "BBMP BPAS Portal (ಬಿಬಿಎಂಪಿ ಬಿಪಿಎಎಸ್)",
          "item": "https://sarva-dharma.github.io/srisaienterprises/#bbmp-bpas-portal"
        },
        {
          "@type": "ListItem",
          "position": 6,
          "name": "Knowledge Hub (ಮಾಹಿತಿ ಕೋಶ)",
          "item": "https://sarva-dharma.github.io/srisaienterprises/#knowledge-hub"
        }
      ]
    },
    {
      "@type": ["Product", "Service"],
      "@id": "https://sarva-dharma.github.io/srisaienterprises/#product-plan-sanction",
      "name": "Building Plan Sanctions & Approvals (BBMP / GBA / BDA)",
      "alternateName": "ಕಟ್ಟಡ ನಕ್ಷೆ ಮಂಜೂರಾತಿ ಮತ್ತು ಅನುಮೋದನೆ",
      "description": "End-to-end statutory building plan approval across Greater Bengaluru Authority (GBA), BBMP 8 zones, BDA, and BIAAPA with Nambike Nakshe fast-track provisional sanction under Sakala 14-21 days guarantee.",
      "category": "Municipal Approvals",
      "brand": {
        "@type": "Brand",
        "name": "Sri Sai Enterprises"
      },
      "offers": {
        "@type": "Offer",
        "url": "https://sarva-dharma.github.io/srisaienterprises/#services",
        "price": "35000.00",
        "priceCurrency": "INR",
        "availability": "https://schema.org/InStock",
        "itemCondition": "https://schema.org/NewCondition",
        "priceValidUntil": "2027-12-31",
        "seller": {
          "@id": "https://sarva-dharma.github.io/srisaienterprises/#store"
        }
      }
    },
    {
      "@type": ["Product", "Service"],
      "@id": "https://sarva-dharma.github.io/srisaienterprises/#product-predcr-cad",
      "name": "AutoDCR & PreDCR CAD Layer Scrutiny Drafting",
      "alternateName": "ಆಟೋಡಿಸಿಆರ್ ಮತ್ತು ಪ್ರಿಡಿಸಿಆರ್ ಸಿಎಡಿ ವಿನ್ಯಾಸ",
      "description": "Mathematically exact architectural drafting conforming to municipal PreDCR software layers (_RES_BLT, _SETBACK, _ROAD) guaranteeing zero automated rejections on bpas.bbmpgov.in.",
      "category": "CAD Engineering",
      "brand": {
        "@type": "Brand",
        "name": "Sri Sai Enterprises"
      },
      "offers": {
        "@type": "Offer",
        "url": "https://sarva-dharma.github.io/srisaienterprises/#services",
        "price": "22000.00",
        "priceCurrency": "INR",
        "availability": "https://schema.org/InStock",
        "itemCondition": "https://schema.org/NewCondition",
        "priceValidUntil": "2027-12-31",
        "seller": {
          "@id": "https://sarva-dharma.github.io/srisaienterprises/#store"
        }
      }
    },
    {
      "@type": ["Product", "Service"],
      "@id": "https://sarva-dharma.github.io/srisaienterprises/#product-ekhata",
      "name": "e-Khata Digital Registration & B-Khata to A-Khata Conversion",
      "alternateName": "ಇ-ಖಾತಾ ನೋಂದಣಿ & ಖಾತಾ ವರ್ಗಾವಣೆ",
      "description": "Official e-Aasthi digital e-Khata certificate issuance, Khata transfer, title verification, and B-Khata betterment payment facilitation across Bengaluru.",
      "category": "Property Titling",
      "brand": {
        "@type": "Brand",
        "name": "Sri Sai Enterprises"
      },
      "offers": {
        "@type": "Offer",
        "url": "https://sarva-dharma.github.io/srisaienterprises/#services",
        "price": "18000.00",
        "priceCurrency": "INR",
        "availability": "https://schema.org/InStock",
        "itemCondition": "https://schema.org/NewCondition",
        "priceValidUntil": "2027-12-31",
        "seller": {
          "@id": "https://sarva-dharma.github.io/srisaienterprises/#store"
        }
      }
    },
    {
      "@type": ["Product", "Service"],
      "@id": "https://sarva-dharma.github.io/srisaienterprises/#product-architectural-design",
      "name": "Architectural Working Drawings & 3D Elevation Modeling",
      "alternateName": "ವಾಸ್ತುಶಿಲ್ಪ ವಿನ್ಯಾಸ ಮತ್ತು 3D ಎಲಿವೇಶನ್",
      "description": "Council of Architecture registered custom floor plans, 3D exterior facade renders, Vastu Purusha Mandala alignment, and certified structural stability packages.",
      "category": "Architecture & Engineering",
      "brand": {
        "@type": "Brand",
        "name": "Sri Sai Enterprises"
      },
      "offers": {
        "@type": "Offer",
        "url": "https://sarva-dharma.github.io/srisaienterprises/#services",
        "price": "45000.00",
        "priceCurrency": "INR",
        "availability": "https://schema.org/InStock",
        "itemCondition": "https://schema.org/NewCondition",
        "priceValidUntil": "2027-12-31",
        "seller": {
          "@id": "https://sarva-dharma.github.io/srisaienterprises/#store"
        }
      }
    },
    {
      "@type": ["Product", "Service"],
      "@id": "https://sarva-dharma.github.io/srisaienterprises/#product-statutory-noc",
      "name": "Statutory Government NOC Procurement & Clearances",
      "alternateName": "ಸರ್ಕಾರಿ ಎನ್‌ಒಸಿ ಕ್ಲಿಯರೆನ್ಸ್ ಮತ್ತು ಅನುಮೋದನೆ",
      "description": "End-to-end statutory liaisoning for Karnataka Fire & Emergency NOC, AAI/HAL Airport Height clearance (NOCAS), BWSSB water line, and BESCOM electrical load sanction.",
      "category": "Liaisoning",
      "brand": {
        "@type": "Brand",
        "name": "Sri Sai Enterprises"
      },
      "offers": {
        "@type": "Offer",
        "url": "https://sarva-dharma.github.io/srisaienterprises/#services",
        "price": "30000.00",
        "priceCurrency": "INR",
        "availability": "https://schema.org/InStock",
        "itemCondition": "https://schema.org/NewCondition",
        "priceValidUntil": "2027-12-31",
        "seller": {
          "@id": "https://sarva-dharma.github.io/srisaienterprises/#store"
        }
      }
    },
    {
      "@type": ["Product", "Service"],
      "@id": "https://sarva-dharma.github.io/srisaienterprises/#product-turnkey-construction",
      "name": "Turnkey Residential Construction & Structural Build",
      "alternateName": "ಕಟ್ಟಡ ನಿರ್ಮಾಣ ಮತ್ತು ವಾಸ್ತುಶಿಲ್ಪ ವಿನ್ಯಾಸ",
      "description": "Comprehensive residential and commercial turnkey construction packages (₹1,950 to ₹3,400/sq.ft) with quality testing, plinth-to-finish supervision, and OC clearance.",
      "category": "Architecture & Build",
      "brand": {
        "@type": "Brand",
        "name": "Sri Sai Enterprises"
      },
      "offers": {
        "@type": "Offer",
        "url": "https://sarva-dharma.github.io/srisaienterprises/#services",
        "price": "50000.00",
        "priceCurrency": "INR",
        "availability": "https://schema.org/InStock",
        "itemCondition": "https://schema.org/NewCondition",
        "priceValidUntil": "2027-12-31",
        "seller": {
          "@id": "https://sarva-dharma.github.io/srisaienterprises/#store"
        }
      }
    },
    {
      "@type": "FAQPage",
      "@id": "https://sarva-dharma.github.io/srisaienterprises/#faq",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "Where is Sri Sai Enterprises located in Bengaluru?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Sri Sai Enterprises is located at #3309, 1st Main Road, Gayathrinagar, Bangalore - 560021, directly opposite More Retail Store. Walk-in consultations are welcome for building plan sanctions, AutoDCR CAD drafting, and property e-Khata processing."
          }
        },
        {
          "@type": "Question",
          "name": "What are the office working hours and consultation timings?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "The studio is open Monday through Saturday from 9:30 AM to 7:30 PM (IST). The office is closed on Sundays. Online inquiries, WhatsApp assistance (+91 94480 54185), and Sakala client portal tracking are available 24/7."
          }
        },
        {
          "@type": "Question",
          "name": "How long does building plan sanction approval take in Bengaluru?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Under the Karnataka Sakala Guarantee, building plan sanctions take 14 to 21 business days for standard BBMP BPAS approvals. For eligible residential plots up to 50x80 ft under the Nambike Nakshe trust-and-verify self-certification scheme, provisional plan sanctions are issued within 3 to 7 business days."
          }
        },
        {
          "@type": "Question",
          "name": "What payment methods and currencies are accepted at Sri Sai Enterprises?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Sri Sai Enterprises accepts Indian Rupee (INR) payments via UPI (Google Pay, PhonePe, Paytm), Net Banking / IMPS / NEFT, Credit and Debit Cards, Cheque, and Cash at the studio. Official tax invoices and government treasury challan receipts from BBMP BPAS are provided."
          }
        },
        {
          "@type": "Question",
          "name": "What architectural and municipal sanction services are provided by Sri Sai Enterprises?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Sri Sai Enterprises provides end-to-end building plan approvals (BBMP BPAS, GBA, BDA, BIAAPA, STRR), PreDCR/AutoDCR CAD drafting, Commencement Certificate (CC) and Occupancy Certificate (OC) clearances, e-Khata registration and B-Khata to A-Khata betterment conversions, architectural 2D/3D design, cost estimation BOQs, and large-format architectural blueprints."
          }
        },
        {
          "@type": "Question",
          "name": "What are the credentials and experience of Sri Sai Enterprises?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Established in 1989, Sri Sai Enterprises has over 37 years of uninterrupted architectural and municipal liaisoning heritage in Bengaluru, having delivered 23,000+ approved sanctions. The firm is led by S. M. Thyagaraja (COA Reg. CA/2009/44120, BBMP Approved Supervisor Lic. BCC/BL-3.2.3/S-218/89-90)."
          }
        }
      ]
    },
    {
      "@type": "WebPage",
      "@id": "https://sarva-dharma.github.io/srisaienterprises/#webpage",
      "url": "https://sarva-dharma.github.io/srisaienterprises/",
      "name": "Sri Sai Enterprises | Building Plan Approvals & Architecture in Bengaluru Since 1989",
      "isPartOf": {
        "@id": "https://sarva-dharma.github.io/srisaienterprises/#website"
      },
      "about": {
        "@id": "https://sarva-dharma.github.io/srisaienterprises/#store"
      },
      "inLanguage": ["en-IN", "kn-IN"],
      "speakable": {
        "@type": "SpeakableSpecification",
        "cssSelector": [
          "#audience-navigator h2",
          "#services h2",
          "#about-founder h3",
          "#fee-estimator h2"
        ]
      }
    }
  ]
}

# Validate JSON serialization
json_str = json.dumps(schema_data, indent=2, ensure_ascii=False)
loaded = json.loads(json_str)

print("SUCCESS: JSON-LD Schema is completely valid JSON.")
print(f"Total Graph Entities: {len(loaded['@graph'])}")
for i, entity in enumerate(loaded['@graph']):
    types = entity.get('@type')
    eid = entity.get('@id', 'no-id')
    name = entity.get('name', 'unnamed')
    print(f"  [{i+1}] Type: {types} | ID: {eid} | Name: {name}")
