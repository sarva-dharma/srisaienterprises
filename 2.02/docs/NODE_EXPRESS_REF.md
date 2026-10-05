# Node.js / Express Backend Architecture Reference

For developers deploying to an existing Node.js runtime or cloud environment (e.g. AWS Lambda, Vercel, Node Container), here is the modular architecture, Prisma schema, and Express router configuration mirroring the Python backend.

---

## 1. Prisma Schema (`prisma/schema.prisma`)

```prisma
datasource db {
  provider = "postgresql" // or "sqlite"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}

enum Role {
  ADMIN
  ARCHITECT
  CLIENT
}

enum LeadStatus {
  NEW
  CONTACTED
  QUOTATION_SENT
  CONVERTED
  ARCHIVED
}

model User {
  id           Int       @id @default(autoincrement())
  name         String
  email        String    @unique
  passwordHash String
  role         Role      @default(CLIENT)
  phone        String?
  createdAt    DateTime  @default(now())
  projects     Project[]
}

model Service {
  id                 Int      @id @default(autoincrement())
  title              String
  slug               String   @unique
  category           String   @default("Approval")
  shortDesc          String
  fullDesc           String
  icon               String   @default("building")
  baseFee            Float    @default(15000)
  bettermentRateSqft Float    @default(250)
  scrutinyRateSqft   Float    @default(3.5)
  turnaroundDays     String   @default("14-21 Days")
  isActive           Boolean  @default(true)
  displayOrder       Int      @default(0)
  features           String[] // Stored as array or JSON string
  createdAt          DateTime @default(now())
  leads              Lead[]
}

model Lead {
  id             Int        @id @default(autoincrement())
  fullName       String
  email          String
  phone          String
  plotLocation   String?
  plotDimensions String?
  serviceId      Int?
  service        Service?   @relation(fields: [serviceId], references: [id])
  serviceTitle   String?
  message        String?
  status         LeadStatus @default(NEW)
  internalNotes  String?
  createdAt      DateTime   @default(now())
  updatedAt      DateTime   @updatedAt
}

model Project {
  id                    Int               @id @default(autoincrement())
  referenceNo           String            @unique // e.g. SAKALA-GBA-2026-0894
  clientId              Int
  client                User              @relation(fields: [clientId], references: [id])
  clientName            String
  title                 String
  plotLocation          String
  wardNo                String?
  surveyNo              String?
  authority             String            @default("GBA / BBMP")
  currentStage          String            @default("Drafting")
  nambikeNaksheEligible Boolean           @default(false)
  plotAreaSqft          Float             @default(1200)
  builtupAreaSqft       Float             @default(2400)
  assignedArchitect     String
  completionPercent     Int               @default(20)
  remarks               String?
  createdAt             DateTime          @default(now())
  updatedAt             DateTime          @updatedAt
  timelines             ProjectTimeline[]
  documents             ProjectDocument[]
}

model ProjectTimeline {
  id          Int      @id @default(autoincrement())
  projectId   Int
  project     Project  @relation(fields: [projectId], references: [id], onDelete: Cascade)
  stageName   String
  status      String   @default("pending") // completed, in_progress, pending
  dateUpdated String?
  remarks     String?
}

model ProjectDocument {
  id              Int      @id @default(autoincrement())
  projectId       Int
  project         Project  @relation(fields: [projectId], references: [id], onDelete: Cascade)
  title           String
  docType         String   @default("OTHER") // CAD_DWG, SANCTION_CERT, E_KHATA, NOC
  filename        String
  filePath        String
  fileSizeDisplay String   @default("1.5 MB")
  isDownloadable  Boolean  @default(true)
  uploadedAt      DateTime @default(now())
}
```

---

## 2. Express Server (`server.js`)

```javascript
import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import jwt from 'jsonwebtoken';
import bcrypt from 'bcryptjs';
import { PrismaClient } from '@prisma/client';

dotenv.config();
const app = express();
const prisma = new PrismaClient();

app.use(cors());
app.use(express.json());

// Public: Get Active Services
app.get('/api/services', async (req, res) => {
  const services = await prisma.service.findMany({
    where: { isActive: true },
    orderBy: { displayOrder: 'asc' }
  });
  res.json({ count: services.length, services });
});

// Public: Capture Lead (Book Consultation)
app.post('/api/leads', async (req, res) => {
  const { fullName, email, phone, plotLocation, plotDimensions, message, serviceTitle } = req.body;
  if (!fullName || !phone) {
    return res.status(400).json({ error: 'Full name and phone are required' });
  }
  const lead = await prisma.lead.create({
    data: { fullName, email, phone, plotLocation, plotDimensions, message, serviceTitle }
  });
  res.status(201).json({ message: 'Consultation request received', leadId: lead.id });
});

// Client Portal: Track Application Status by Reference Number
app.get('/api/client/projects', async (req, res) => {
  const { referenceNo } = req.query;
  if (referenceNo) {
    const project = await prisma.project.findUnique({
      where: { referenceNo: String(referenceNo) },
      include: { timelines: true, documents: true }
    });
    if (!project) return res.status(404).json({ error: 'Application reference not found' });
    return res.json({ projects: [project] });
  }
  res.status(400).json({ error: 'Reference number required' });
});

// Admin: Update Project Stage (PreDCR -> AutoDCR -> Approved)
app.patch('/api/admin/projects/:id/stage', async (req, res) => {
  const { id } = req.params;
  const { stage, remarks } = req.body;

  const stagePercentages = {
    'Drafting': 20,
    'PreDCR Scrutiny': 40,
    'AutoDCR Submission': 60,
    'Site Inspection': 75,
    'NOC Clearance': 85,
    'Approved': 100
  };

  const updatedProject = await prisma.project.update({
    where: { id: Number(id) },
    data: {
      currentStage: stage,
      completionPercent: stagePercentages[stage] || 50,
      remarks
    },
    include: { timelines: true, documents: true }
  });

  res.json({ message: `Stage advanced to ${stage}`, project: updatedProject });
});

app.listen(process.env.PORT || 5000, () => {
  console.log(`Node/Express Sanctions API running on port ${process.env.PORT || 5000}`);
});
```
