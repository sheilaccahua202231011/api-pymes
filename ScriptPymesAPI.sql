DROP DATABASE IF EXISTS bd_api_pymes;
CREATE DATABASE bd_api_pymes CHARSET utf8mb4;
USE bd_api_pymes;

CREATE TABLE Pymes (
    pymesId INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    total_employee INT NOT NULL,
    average_age INT NOT NULL,
    is_private BOOLEAN NOT NULL,
    bedded INT NOT NULL,
    is_sorted_ascending BOOLEAN NOT NULL,
    register_date DATE
);

CREATE TABLE Products (
    productId INT AUTO_INCREMENT PRIMARY KEY,
    pymesId INT NOT NULL,
    coverage INT NOT NULL,
    product_name VARCHAR(255),
    product_options VARCHAR(255),    
    top_feature VARCHAR(255),
    inpatient VARCHAR(255),
    outpatient_gp VARCHAR(255),
    outpatient_sp VARCHAR(255),
    outpatient_dental VARCHAR(255),
    personal_accident VARCHAR(255),
    term_life VARCHAR(255),
    critical_illness VARCHAR(255),
    premium_per_pax DECIMAL,
    total_premium DECIMAL,
    FOREIGN KEY (coverageId) REFERENCES Coverage(coverageId),
    FOREIGN KEY (pymesId) REFERENCES Pymes(pymesId)
);

CREATE TABLE Coverage (
    coverageId INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    productId INT NOT NULL,
    outpatient_gp BOOLEAN,
    outpatient_sp BOOLEAN,
    outpatient_dental BOOLEAN,
    personal_accident BOOLEAN,
    term_life BOOLEAN,
    critical_illness BOOLEAN,
    FOREIGN KEY (productId) REFERENCES Products(productId)
);

CREATE TABLE Inpatient (
    inpatientId INT AUTO_INCREMENT PRIMARY KEY,
    coverageId INT NOT NULL,
    min_limit DECIMAL,
    max_limit DECIMAL,
    FOREIGN KEY (coverageId) REFERENCES Coverage(coverageId)
);

CREATE TABLE OutpatientDental (
    outpatientdentalId INT AUTO_INCREMENT PRIMARY KEY,
    coverageId INT NOT NULL,
    min_limit DECIMAL,
    max_limit DECIMAL,
    FOREIGN KEY (coverageId) REFERENCES Coverage(coverageId)
);

CREATE TABLE PersonalAccident (
    personalaccidentId INT AUTO_INCREMENT PRIMARY KEY,
    coverageId INT NOT NULL,
    min_limit DECIMAL,
    max_limit DECIMAL,
    FOREIGN KEY (coverageId) REFERENCES Coverage(coverageId)
);

CREATE TABLE TermLife (
    termlifeId INT AUTO_INCREMENT PRIMARY KEY,
    coverageId INT NOT NULL,
    min_limit DECIMAL,
    max_limit DECIMAL,
    FOREIGN KEY (coverageId) REFERENCES Coverage(coverageId)
);

CREATE TABLE CriticalIllness (
    criticalillnessId INT AUTO_INCREMENT PRIMARY KEY,
    coverageId INT NOT NULL,
    min_limit DECIMAL,
    max_limit DECIMAL,
    FOREIGN KEY (coverageId) REFERENCES Coverage(coverageId)
);

