
def langProbeTables():
    
    sql_createtable_dataIV =           """
                                        CREATE TABLE IF NOT EXISTS dataIV (
                                        ID INT AUTO_INCREMENT PRIMARY KEY,
                                        `ID del proyecto` VARCHAR(255),
                                        Voltage VARCHAR(1100),
                                        Current VARCHAR(1100),
                                        `std Voltage` VARCHAR(1100),
                                        `std Current` VARCHAR(1100)
                                        )
                                        """
                                        
    sql_createtable_dataParameters =   """
                                        CREATE TABLE IF NOT EXISTS dataParameters (
                                        ID INT AUTO_INCREMENT PRIMARY KEY,
                                        `ID del proyecto` VARCHAR(255),
                                        `Je [A/m^2]` FLOAT,
                                        `Jp [A/m^2]` FLOAT,
                                        `Ldebye [µm]` FLOAT,
                                        `Ne [m^-3]` FLOAT,	
                                        `Ni [m^-3]` FLOAT,	
                                        `Vf [V]` FLOAT,	
                                        `Vp [V]` FLOAT,	
                                        `Vpmax [V]` FLOAT,	
                                        `Vsat [V]` FLOAT,	
                                        `eedf_AvgEnergy [eV]` FLOAT,	
                                        `eedf_Ne [m^-3]` FLOAT,	
                                        `eedf_kTe [eV]` FLOAT,	
                                        `isat [mA]` FLOAT,	
                                        `kTe [eV]` FLOAT
                                        )
                                        """
                                        
    sql_createtable_dataSettings =     """
                                        CREATE TABLE IF NOT EXISTS dataSettings (
                                        ID INT AUTO_INCREMENT PRIMARY KEY,
                                        `ID del proyecto` VARCHAR(255),
                                        VsatFactor FLOAT,
                                        bUse2ndDerivativeZeroVp FLOAT,
                                        bUseUserVp FLOAT,
                                        correctDC FLOAT,
                                        electronReflectVoltage VARCHAR(255),
                                        endCrop FLOAT,
                                        `gas_temperature [K]` FLOAT,
                                        `ionmass [g/mol]` FLOAT,
                                        kfactor FLOAT,
                                        nDerivativePoints FLOAT,
                                        offsetCurrent FLOAT,
                                        `pressure [Torr]` FLOAT,
                                        `probe_holder [m]` FLOAT,
                                        `probe_length [m]` FLOAT,
                                        `probe_radius [m]` FLOAT,
                                        `probe_resistance [Ohm]` FLOAT,
                                        `setVp [V]` FLOAT,
                                        sigmaEn FLOAT,
                                        sigmaN FLOAT,
                                        startCrop FLOAT
                                        )
                                        """
                                        
    sql_createtable_dataExtra =         """
                                            CREATE TABLE IF NOT EXISTS dataExtra (
                                            ID INT AUTO_INCREMENT PRIMARY KEY,
                                            `ID del proyecto` VARCHAR(255),
                                            date VARCHAR(255),
                                            deviceID VARCHAR(255),
                                            time VARCHAR(255),
                                            `Name file` VARCHAR(255),	
                                            Description VARCHAR(255),
                                            Comment VARCHAR(255)
                                            )
                                        """
                            
    return [sql_createtable_dataIV,sql_createtable_dataParameters,sql_createtable_dataSettings,sql_createtable_dataExtra]

def ProjectTable():
    
    sql_createtable_project =           """
                                            CREATE TABLE IF NOT EXISTS projects (
                                            `ID del proyecto` VARCHAR(255) PRIMARY KEY,
                                            Usuario VARCHAR(255),
                                            `Nombre del proyecto` VARCHAR(255),
                                            `Fecha de creación` VARCHAR(255),
                                            Descripción VARCHAR(255)	
                                            )
                                        """
    
    return sql_createtable_project