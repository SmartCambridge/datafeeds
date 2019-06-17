</omit>

IDOX
====

<omit>

To leave out the 'omit' sections:

```
awk '/<\/omit>/,/<omit>/' NOTES.md | grep -v 'omit>' > idox_summary.md
```

For access to the DatexII feed:

Uid : CambsUni
Pwd : P8MSatsW9L3

For access to the test site http://www.cambsvoyager.com/datexii/TestInterface.aspx :

uid : Testaccess
pwd : 5dhwRQ3y7WNcgLes

Note that the test interface then needs DatexII feed ID/Pwd above.

</omit>

Available data
--------------

Based on the CloudAmber document "UTMC Data Exchange Product Specification", IDOX potentially gives
access to 15 information feeds and 6 feeds of 'Predefined Locations'
- see table 5.1 on pages 30-32.

These 6 information feeds and 5 'Predefined Locations' feeds appear to
contain useful information and are described further below:

* Road Works
* Traffic Data
* Variable Message Sign
* Car Park( DatexII version 1.0 )
* Car Park( DatexII version 2.2.0 )
* CCTV
* Predefined Locations - Traffic Data Links
* Predefined Locations - Traffic Data Section
* Predefined Locations - VMS
* Predefined Locations - Journey Time Sections
* Predefined Locations - CCTV

The remaining 9 information feeds and 1 feed of 'Predefined Locations' return either a response containing no useful data, or
a completely empty response, or a 'Not found' error:

* Events
* Traffic Data Extension
* Journey Times- Current
* Journey Times- Predictive
* Cycle Hubs
* EV Charging Points
* Walkers Facilities
* Point Of Interest
* Meteorological
* Predefined Locations - Matrix

Road Works
----------

3097 records giving location, description, and time period (ranging from 2009-11-01T00:00:00 to 2024-04-09T23:59:59).

<omit>

```
http --auth CambsUni:P8MSatsW9L3 get http://91.151.215.136/CloudAmber/CambsDateXII/pox/GetDateXIIRoadWorks Easting==0 EastingEnd==999999 Northing==0 NorthingEnd==999999 startDate==01-May-2019 endDate==30-May-2019

xmlstarlet sel -N d=http://datex2.eu/schema/1_0/1_0 -t -m '//d:situation' -m 'd:situationRecord/d:validity/d:validityTimeSpecification' -v 'd:overallEndTime' -n RoadWorks.xml | sort | less

xmlstarlet sel -N d=http://datex2.eu/schema/1_0/1_0 -t -v 'count(//d:situation)' -n RoadWorks.xml
```

```
<?xml version="1.0" encoding="utf-8"?>
<d2LogicalModel xmlns="http://datex2.eu/schema/1_0/1_0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" modelBaseVersion="1.0">
  <exchange>
    <supplierIdentification>
      <country>gb</country>
      <nationalIdentifier>Cambridgeshire County</nationalIdentifier>
    </supplierIdentification>
  </exchange>
  <payloadPublication xsi:type="SituationPublication" lang="en">
    <publicationTime>2019-06-11T14:09:55+01:00</publicationTime>
    <publicationCreator>
      <country>gb</country>
      <nationalIdentifier>Cambridgeshire County</nationalIdentifier>
    </publicationCreator>
    <situation id="GUID0">
      <headerInformation>
        <confidentiality>restrictedToAuthoritiesTrafficOperatorsAndPublishers</confidentiality>
        <informationUsage>broadcast</informationUsage>
        <informationStatus>real</informationStatus>
      </headerInformation>
      <situationRecord xsi:type="MaintenanceWorks" id="GUIDAD00155700032/1-1">
        <situationRecordCreationTime>2019-04-18T15:38:37</situationRecordCreationTime>
        <situationRecordVersion>1</situationRecordVersion>
        <situationRecordVersionTime>2019-04-19T02:03:46</situationRecordVersionTime>
        <situationRecordFirstSupplierVersionTime>2019-04-18T15:38:37</situationRecordFirstSupplierVersionTime>
        <probabilityOfOccurrence>certain</probabilityOfOccurrence>
        <sourceInformation>
          <sourceName>
            <value lang="en">Cambridgeshire Government</value>
          </sourceName>
        </sourceInformation>
        <validity>
          <validityStatus>active</validityStatus>
          <validityTimeSpecification>
            <overallStartTime>2019-07-31T00:00:00</overallStartTime>
            <overallEndTime>2019-08-01T23:59:59</overallEndTime>
            <validPeriod>
              <startOfPeriod>2019-07-31T00:00:00</startOfPeriod>
              <endOfPeriod>2019-08-01T23:59:59</endOfPeriod>
            </validPeriod>
          </validityTimeSpecification>
        </validity>
        <impact>
          <impactOnTraffic>heavy</impactOnTraffic>
        </impact>
        <nonGeneralPublicComment>
          <comment>
            <value lang="en">Anglian Water - All Areas Use of two way traffic lights to complete PPM on Vacuum pots. Vac pots to be cleaned out by use of a jetter. Opening of manhole covers only no breaking of road surface. Traffic management to be completed by A Plant by use of 2 way traffic lights.  TRAFFIC MANAGEMENT TYPE  = None / signing only</value>
          </comment>
          <commentExtension>
            <nonGeneralPublicCommentExtension xmlns="">
              <shortDescription>
                <description>
                  <value lang="en">Use of two way traffic lights to complete PPM on V</value>
                </description>
              </shortDescription>
              <name>
                <description>
                  <value lang="en">Use of two way traffic lights to complete PPM on Vacuum pots. Vac pots to be cleaned out by use of a jetter. Opening of manhole covers only no breaking of road surface. Traffic management to be completed by A Plant by use of 2 way traffic lights.</value>
                </description>
              </name>
            </nonGeneralPublicCommentExtension>
          </commentExtension>
        </nonGeneralPublicComment>
        <groupOfLocations>
          <locationContainedInGroup xsi:type="Point">
            <tpegpointLocation xsi:type="TPEGSimplePoint">
              <tpegDirection>other</tpegDirection>
              <tpegLocationType>intersection</tpegLocationType>
              <point xsi:type="TPEGJunction">
                <pointCoordinates>
                  <latitude>52.6420822</latitude>
                  <longitude>-0.244219869</longitude>
                </pointCoordinates>
                <name>
                  <descriptor>
                    <value lang="en">1-23 werrington bridge road</value>
                  </descriptor>
                  <tpegDescriptorType>junctionName</tpegDescriptorType>
                </name>
                <ilc>
                  <descriptor>
                    <value lang="en"/>
                  </descriptor>
                  <tpegDescriptorType>tpegILCName1</tpegDescriptorType>
                </ilc>
              </point>
            </tpegpointLocation>
          </locationContainedInGroup>
        </groupOfLocations>
        <effectOnRoadLayout>roadLayoutUnchanged</effectOnRoadLayout>
        <roadMaintenanceType>other</roadMaintenanceType>
      </situationRecord>
    </situation>
    ...
  </payloadPublication>
</d2LogicalModel>
```

```
http get --auth CambsUni:P8MSatsW9L3 http://91.151.215.136/CloudAmber/Cambs1DateXII/Json/GetDateXIIEvents Easting==0 EastingEnd==999999 Northing==0 NorthingEnd==999999 startDate==01-May-2019 endDate==30-May-2019
```

```
{
  "d": {
    "__type": "D2LogicalModel:#CloudAmber.DatexII",
    "d2LogicalModelExtensionField": null,
    "exchangeField": {
      "__type": "Exchange:#CloudAmber.DatexII",
      "catalogueReferenceField": null,
      "changedFlagField": 0,
      "changedFlagFieldSpecified": false,
      "clientIdentificationField": null,
      "deliveryBreakField": false,
      "deliveryBreakFieldSpecified": false,
      "denyReasonField": 0,
      "denyReasonFieldSpecified": false,
      "exchangeExtensionField": null,
      "filterReferenceField": null,
      "historicalStartDateField": null,
      "historicalStopDateField": null,
      "keepAliveField": false,
      "keepAliveFieldSpecified": false,
      "requestTypeField": 0,
      "requestTypeFieldSpecified": false,
      "responseField": 0,
      "responseFieldSpecified": false,
      "subscriptionField": null,
      "subscriptionReferenceField": null,
      "supplierIdentificationField": {
        "__type": "InternationalIdentifier:#CloudAmber.DatexII",
        "countryField": 14,
        "internationalIdentifierExtensionField": null,
        "nationalIdentifierField": "Cambridgeshire County"
      },
      "targetField": null
    },
    "modelBaseVersionField": "1.0",
    "payloadPublicationField": {
      "__type": "SituationPublication:#CloudAmber.DatexII",
      "feedTypeField": null,
      "langField": "en",
      "payloadPublicationExtensionField": null,
      "publicationCreatorField": {
        "__type": "InternationalIdentifier:#CloudAmber.DatexII",
        "countryField": 14,
        "internationalIdentifierExtensionField": null,
        "nationalIdentifierField": "Cambridgeshire County"
      },
      "publicationTimeField": {
        "__type": "DateTime:#CloudAmber.DatexII",
        "valueField": "/Date(1560258595000+0100)/"
      },
      "situationField": [
        {
          "__type": "Situation:#CloudAmber.DatexII",
          "headerInformationField": {
            "__type": "HeaderInformation:#CloudAmber.DatexII",
            "areaOfInterestField": 1,
            "areaOfInterestFieldSpecified": false,
            "confidentialityField": 4,
            "headerInformationExtensionField": null,
            "informationStatusField": 0,
            "informationUsageField": [
              0
            ],
            "urgencyField": 0,
            "urgencyFieldSpecified": false
          },
          "idField": "GUID0",
          "overallImpactField": 0,
          "overallImpactFieldSpecified": false,
          "relatedSituationField": null,
          "situationExtensionField": null,
          "situationRecordField": [
            {
              "__type": "MaintenanceWorks:#CloudAmber.DatexII",
              "adviceField": null,
              "causeField": null,
              "generalPublicCommentField": null,
              "groupOfLocationsField": {
                "__type": "GroupOfLocations:#CloudAmber.DatexII",
                "groupOfLocationsExtensionField": null,
                "locationContainedInGroupField": [
                  {
                    "__type": "Point:#CloudAmber.DatexII",
                    "locationExtensionField": null,
                    "destinationField": null,
                    "networkLocationExtensionField": null,
                    "supplementaryPositionalDescriptionField": null,
                    "alertCPointField": null,
                    "pointByCoordinatesField": null,
                    "pointExtensionField": null,
                    "referencePointField": null,
                    "tpegpointLocationField": {
                      "__type": "TPEGSimplePoint:#CloudAmber.DatexII",
                      "tpegDirectionField": 16,
                      "tpegpointLocationExtensionField": null,
                      "pointField": {
                        "__type": "TPEGJunction:#CloudAmber.DatexII",
                        "ilcField": [
                          {
                            "__type": "TPEGILCPointDescriptor:#CloudAmber.DatexII",
                            "descriptorField": [
                              {
                                "__type": "TPEGDescriptorValue:#CloudAmber.DatexII",
                                "langField": "en",
                                "valueField": ""
                              }
                            ],
                            "tpegdescriptorExtensionField": null,
                            "tpegpointDescriptorExtensionField": null,
                            "tpegDescriptorTypeField": 0,
                            "tpegilcpointDescriptorExtensionField": null
                          }
                        ],
                        "nameField": {
                          "__type": "TPEGJunctionPointDescriptor:#CloudAmber.DatexII",
                          "descriptorField": [
                            {
                              "__type": "TPEGDescriptorValue:#CloudAmber.DatexII",
                              "langField": "en",
                              "valueField": "1-23 werrington bridge road"
                            }
                          ],
                          "tpegdescriptorExtensionField": null,
                          "tpegpointDescriptorExtensionField": null,
                          "tpegDescriptorTypeField": 0,
                          "tpegjunctionPointDescriptorExtensionField": null
                        },
                        "otherNameField": null,
                        "pointCoordinatesField": {
                          "__type": "PointCoordinates:#CloudAmber.DatexII",
                          "latitudeField": 52.6420822,
                          "longitudeField": -0.244219869,
                          "pointCoordinatesExtensionField": null
                        },
                        "tpegjunctionExtensionField": null
                      },
                      "tpegLocationTypeField": 0,
                      "tpegsimplePointExtensionField": null
                    }
                  }
                ],
                "routeDestinationField": null
              },
              "idField": "GUIDAD00155700032/1-1",
              "impactField": {
                "__type": "Impact:#CloudAmber.DatexII",
                "delaysField": null,
                "impactDetailsField": null,
                "impactExtensionField": null,
                "impactOnTrafficField": 2,
                "impactOnTrafficFieldSpecified": true
              },
              "informationUsageOverrideField": 0,
              "informationUsageOverrideFieldSpecified": false,
              "managementField": null,
              "nonGeneralPublicCommentField": [
                {
                  "__type": "Comment:#CloudAmber.DatexII",
                  "commentDateTimeField": null,
                  "commentExtensionField": {
                    "__type": "ExtensionType:#CloudAmber.DatexII",
                    "anyField": [
                      "<nonGeneralPublicCommentExtension xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\"><shortDescription><description><value lang=\"en\">Use of two way traffic lights to complete PPM on V</value></description></shortDescription><name><description><value lang=\"en\">Use of two way traffic lights to complete PPM on Vacuum pots. Vac pots to be cleaned out by use of a jetter. Opening of manhole covers only no breaking of road surface. Traffic management to be completed by A Plant by use of 2 way traffic lights.</value></description></name></nonGeneralPublicCommentExtension>"
                    ]
                  },
                  "commentField": [
                    {
                      "__type": "CommentValue:#CloudAmber.DatexII",
                      "langField": "en",
                      "valueField": "Anglian Water - All Areas Use of two way traffic lights to complete PPM on Vacuum pots. Vac pots to be cleaned out by use of a jetter. Opening of manhole covers only no breaking of road surface. Traffic management to be completed by A Plant by use of 2 way traffic lights.  TRAFFIC MANAGEMENT TYPE  = None / signing only"
                    }
                  ]
                }
              ],
              "probabilityOfOccurrenceField": 0,
              "situationRecordCreationReferenceField": null,
              "situationRecordCreationTimeField": {
                "__type": "DateTime:#CloudAmber.DatexII",
                "valueField": "/Date(1555598317000+0100)/"
              },
              "situationRecordExtensionField": null,
              "situationRecordFirstSupplierVersionTimeField": {
                "__type": "DateTime:#CloudAmber.DatexII",
                "valueField": "/Date(1555598317000+0100)/"
              },
              "situationRecordObservationTimeField": null,
              "situationRecordVersionField": "1",
              "situationRecordVersionTimeField": {
                "__type": "DateTime:#CloudAmber.DatexII",
                "valueField": "/Date(1555635826000+0100)/"
              },
              "sourceInformationField": {
                "__type": "SourceInformation:#CloudAmber.DatexII",
                "reliableField": false,
                "reliableFieldSpecified": false,
                "sourceCountryField": 14,
                "sourceCountryFieldSpecified": false,
                "sourceIdentificationField": null,
                "sourceInformationExtensionField": null,
                "sourceNameField": [
                  {
                    "__type": "SourceInformationValue:#CloudAmber.DatexII",
                    "langField": "en",
                    "valueField": "Cambridgeshire Government"
                  }
                ],
                "sourceTypeField": 0,
                "sourceTypeFieldSpecified": false
              },
              "validityField": {
                "__type": "Validity:#CloudAmber.DatexII",
                "validityExtensionField": null,
                "validityStatusField": 0,
                "validityTimeSpecificationField": {
                  "__type": "OverallPeriod:#CloudAmber.DatexII",
                  "exceptionPeriodField": null,
                  "overallEndTimeField": {
                    "__type": "DateTime:#CloudAmber.DatexII",
                    "valueField": "/Date(1564700399000+0100)/"
                  },
                  "overallPeriodExtensionField": null,
                  "overallStartTimeField": {
                    "__type": "DateTime:#CloudAmber.DatexII",
                    "valueField": "/Date(1564527600000+0100)/"
                  },
                  "validPeriodField": [
                    {
                      "__type": "Period:#CloudAmber.DatexII",
                      "endOfPeriodField": {
                        "__type": "DateTime:#CloudAmber.DatexII",
                        "valueField": "/Date(1564700399000+0100)/"
                      },
                      "periodExtensionField": null,
                      "periodNameField": null,
                      "recurringDayWeekMonthPeriodField": null,
                      "recurringTimePeriodOfDayField": null,
                      "startOfPeriodField": {
                        "__type": "DateTime:#CloudAmber.DatexII",
                        "valueField": "/Date(1564527600000+0100)/"
                      }
                    }
                  ]
                }
              },
              "actionOriginField": 0,
              "actionOriginFieldSpecified": false,
              "operatorActionExtensionField": null,
              "operatorActionStatusField": 0,
              "operatorActionStatusFieldSpecified": false,
              "provisionalField": false,
              "provisionalFieldSpecified": false,
              "associatedMaintenanceVehiclesField": null,
              "effectOnRoadLayoutField": [
                7
              ],
              "mobilityField": null,
              "roadworksDurationField": 0,
              "roadworksDurationFieldSpecified": false,
              "roadworksExtensionField": null,
              "roadworksScaleField": 0,
              "roadworksScaleFieldSpecified": false,
              "subjectTypeOfWorksField": null,
              "underTrafficField": false,
              "underTrafficFieldSpecified": false,
              "urgentRoadworksField": false,
              "urgentRoadworksFieldSpecified": false,
              "maintenanceWorksExtensionField": null,
              "roadMaintenanceTypeField": [
                16
              ]
            }
          ]
        },
        <...>
      ],
      "situationPublicationExtensionField": null
    }
  }
}
```

</omit>

Traffic Data
------------

136 records with timestamps (between 2015-04-24T15:20:00+01:00 and
2019-06-13T09:39:08+01:00, 83 in the last few hours) and a location
(by reference, all unique).

Of these

*   56 are of type 'TrafficFlow' containing a 'vehicleFlow' and with
    location references found in the 'Predefined Locations' feeds for 'Traffic
    Data Links' and 'Journey Time Sections'. 18 were last updated
    in 2015 or 2016. The remaining 38 are being updated in near-realtime and correspond to
    the positions of the Drakewell 'BlueTruth' sensors.
*   18 are of type 'TrafficConcentration' with
    location references found in the 'Predefined Locations' feeds for 'Traffic
    Data Links' and 'Journey Time Sections'. All were last updated in 2015 or 2016 and containing an 'occupancy' value that is always 0.
*   62 are of type 'TravelTimeValue' containing a 'travelTime', a 'freeFlowSpeed' (always 0),
    and a 'freeFlowTravelTime' (always 0) and a location reference found in the 'Predefined Locations' feed for 'Traffic Data Section'. 45 updated in the last few hours. All
    correspond to compound or normal (but not 'link') routes in the Drakewell 'BlueTruth' system.

<omit>

```
http --auth CambsUni:P8MSatsW9L3 get http://91.151.215.136/CloudAmber/CambsDateXII/pox/GetDateXIITrafficData Easting==0 EastingEnd==999999 Northing==0 NorthingEnd==999999

xmlstarlet sel -N d=http://datex2.eu/schema/1_0/1_0 -t -v 'count(//d:elaboratedData)' -n TrafficData.xml

xmlstarlet sel -N d=http://datex2.eu/schema/1_0/1_0 -t -m '//d:elaboratedData' -m 'd:basicDataValue' -v 'd:time' -n TrafficData.xml

xmlstarlet sel -N d=http://datex2.eu/schema/1_0/1_0 -t -m '//d:elaboratedData' -m 'd:basicDataValue' -v '@xsi:type' -o ' ' -v 'd:time' -n TrafficData.xml

xmlstarlet sel -N d=http://datex2.eu/schema/1_0/1_0 -t -m '//d:elaboratedData' -m 'd:basicDataValue[@xsi:type="TrafficFlow"]' -v '@xsi:type' -o ' ' -v 'd:time' -v 'd:vehicleFlow' -n TrafficData.xml

xmlstarlet sel -N d=http://datex2.eu/schema/1_0/1_0 -t -m '//d:elaboratedData' -m 'd:basicDataValue[@xsi:type="TrafficConcentration"]' -v '@xsi:type' -o ' ' -v 'd:time' -v 'd:occupancy' -n TrafficData.xml

xmlstarlet sel -N d=http://datex2.eu/schema/1_0/1_0 -t -m '//d:elaboratedData' -m 'd:basicDataValue[@xsi:type="TravelTimeValue"]' -v '@xsi:type' -o ' ' -v 'd:time' -v 'd:travelTime' -o ' ' -v 'd:freeFlowSpeed' -o ' ' -v 'd:freeFlowTravelTime' -n TrafficData.xm
```

```
<?xml version="1.0" encoding="utf-8"?>
<d2LogicalModel xmlns="http://datex2.eu/schema/1_0/1_0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" modelBaseVersion="1.0">
  <exchange>
    <supplierIdentification>
      <country>gb</country>
      <nationalIdentifier>Cambridgeshire County</nationalIdentifier>
    </supplierIdentification>
  </exchange>
  <payloadPublication xsi:type="ElaboratedDataPublication" lang="en">
    <publicationTime>2019-06-11T17:40:19+01:00</publicationTime>
    <publicationCreator>
      <country>gb</country>
      <nationalIdentifier>Cambridgeshire County</nationalIdentifier>
    </publicationCreator>
    <headerInformation>
      <confidentiality>restrictedToAuthoritiesTrafficOperatorsAndPublishers</confidentiality>
      <informationUsage>broadcast</informationUsage>
      <informationStatus>real</informationStatus>
    </headerInformation>
    <elaboratedData id="GUID-Flow-CAMB-MACSSL208510">
      <sourceInformation>
        <sourceName>
          <value lang="en">Cambridgeshire Government</value>
        </sourceName>
      </sourceInformation>
      <basicDataValue xsi:type="TrafficFlow">
        <time>2019-06-11T17:38:55+01:00</time>
        <affectedLocation>
          <locationContainedInGroup xsi:type="LocationByReference">
            <predefinedLocationReference>LINKCAMB-MACSSL208510</predefinedLocationReference>
          </locationContainedInGroup>
        </affectedLocation>
        <vehicleFlow>684</vehicleFlow>
      </basicDataValue>
    </elaboratedData>
    ...
    <elaboratedData id="GUID-Occupancy-CAMBS-D04311">
      <sourceInformation>
        <sourceName>
          <value lang="en">Cambridgeshire Government</value>
        </sourceName>
      </sourceInformation>
      <basicDataValue xsi:type="TrafficConcentration">
        <time>2016-03-08T11:05:00+00:00</time>
        <affectedLocation>
          <locationContainedInGroup xsi:type="LocationByReference">
            <predefinedLocationReference>LINKCAMBS-D04311</predefinedLocationReference>
          </locationContainedInGroup>
        </affectedLocation>
        <occupancy>0</occupancy>
      </basicDataValue>
    </elaboratedData>
    ...
    <elaboratedData id="GUID-TL-CAMB-9800W6P1UD80">
      <sourceInformation>
        <sourceName>
          <value lang="en">Cambridgeshire Government</value>
        </sourceName>
      </sourceInformation>
      <basicDataValue xsi:type="TravelTimeValue">
        <time>2019-06-03T17:07:55+01:00</time>
        <affectedLocation>
          <locationContainedInGroup xsi:type="LocationByReference">
            <predefinedLocationReference>SectionCAMB-9800W6P1UD80</predefinedLocationReference>
          </locationContainedInGroup>
        </affectedLocation>
        <travelTime>281</travelTime>
        <freeFlowSpeed>0</freeFlowSpeed>
        <freeFlowTravelTime>0</freeFlowTravelTime>
      </basicDataValue>
    </elaboratedData>
</payloadPublication>
</d2LogicalModel>
```

</omit>

Variable Message Sign
---------------------

91 records giving position (by reference, all unique), number of rows and columns, current display,
and a startTime timestamp. The current display value is difficult to interpret,
often consisting of a list of numbers (probably spaces free in unidentified
car parks):

```
<vmsLegend>  360 </vmsLegend>
<vmsLegend>  469 </vmsLegend>
<vmsLegend>  143 </vmsLegend>
<vmsLegend>  695 </vmsLegend>
```

or including what are probably display control characters, e.g.:

```
<vmsLegend>[G42][TR15,26,84,7][CB0,0,0][CF7][FO1]FREE PARKING[TR5,40,105,7][CB0,0,0]
[CF7][FO1]A QUICKER ROUTE[TR8,51,98,7][CB0,0,0][CF7][FO1]INTO CAMBRIDGE
[TR30,7,77,7][CB0,0,0][CF7][FO1][CF3] 433 SPACES[CF2]</vmsLegend>
```

<omit>

```
http --auth CambsUni:P8MSatsW9L3 get http://91.151.215.136/CloudAmber/CambsDateXII/pox/GetDateXIIAllVMS Easting==0 EastingEnd==999999 Northing==0 NorthingEnd==999999

xmlstarlet  sel -N d=http://datex2.eu/schema/1_0/1_0 -t -v 'count(//d:situationRecord)' -n AllVMS.xml

xmlstarlet sel -N d=http://datex2.eu/schema/1_0/1_0 -t -m '//d:situationRecord' -o '*** ' -v 'd:validity/d:validityStatus' -o ' ' -v 'd:validity/d:validityTimeSpecification' -o ' ' -v 'd:vmsLegend' -o ' ' -v 'd:vmsType' -n AllVMS.xml
```


```
<d2LogicalModel xmlns="http://datex2.eu/schema/1_0/1_0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" modelBaseVersion="1.0">
    <exchange>
        <supplierIdentification>
            <country>gb</country>
            <nationalIdentifier>Cambridgeshire County</nationalIdentifier>
        </supplierIdentification>
    </exchange>
    <payloadPublication xsi:type="SituationPublication" lang="en">
        <publicationTime>2019-06-11T19:02:59+01:00</publicationTime>
        <publicationCreator>
            <country>gb</country>
            <nationalIdentifier>Cambridgeshire County</nationalIdentifier>
        </publicationCreator>
        <situation id="GUID-VariableMessageSign">
            <headerInformation>
                <confidentiality>restrictedToAuthoritiesTrafficOperatorsAndPublishers</confidentiality>
                <informationUsage>broadcast</informationUsage>
                <informationStatus>real</informationStatus>
            </headerInformation>
            <situationRecord xsi:type="VariableMessageSignSetting" id="GUIDCAMB-V0078">
                <situationRecordCreationTime>2008-11-01T00:00:00</situationRecordCreationTime>
                <situationRecordVersion>20190613105313</situationRecordVersion>
                <situationRecordVersionTime>2019-06-13T10:53:13</situationRecordVersionTime>
                <situationRecordFirstSupplierVersionTime>2008-11-01T00:00:00</situationRecordFirstSupplierVersionTime>
                <probabilityOfOccurrence>certain</probabilityOfOccurrence>
                <sourceInformation>
                    <sourceName>
                        <value lang="en">Cambridgeshire Government</value>
                    </sourceName>
                </sourceInformation>
                <validity>
                    <validityStatus>active</validityStatus>
                    <validityTimeSpecification>
                        <overallStartTime>2019-06-13T10:53:13</overallStartTime>
                    </validityTimeSpecification>
                </validity>
                <groupOfLocations>
                    <locationContainedInGroup xsi:type="LocationByReference">
                        <predefinedLocationReference>VMSCAMB-V0078</predefinedLocationReference>
                    </locationContainedInGroup>
                </groupOfLocations>
                <reasonForSetting>
                    <value lang="en"/>
                </reasonForSetting>
                <numberOfCharacters>16</numberOfCharacters>
                <numberOfRows>4</numberOfRows>
                <vmsLegend>[G42][TR15,26,84,7][CB0,0,0][CF7][FO1]FREE PARKING[TR5,40,105,7][CB0,0,0][CF7][FO1]A QUICKER ROUTE[TR8,51,98,7][CB0,0,0][CF7][FO1]INTO CAMBRIDGE[TR30,7,77,7][CB0,0,0][CF7][FO1][CF3] 555 SPACES[CF2]</vmsLegend>
                <vmsType>other</vmsType>
            </situationRecord>
      ...
    </situation>
  </payloadPublication>
</d2LogicalModel>
```

</omit>

Car parks (v1.0)
----------------

13 records giving name, location, Occupancy, Status, exitRate, fillRate, totalCapacity
of these car parks:

* Grand Arcade
* Grafton East
* Grafton West
* Park Street
* Queen Anne
* P&R Madingley Road
* P&R Trumpington
* P&R Babraham
* P&R Milton
* P&R Newmarket Rd Front
* P&R Newmarket Rd Rear
* P&R St Ives
* P&R Longstanton

<omit>

```
http --auth CambsUni:P8MSatsW9L3 get http://91.151.215.136/CloudAmber/CambsDateXII/pox/GetDateXIICarPark Easting==0 EastingEnd==999999 Northing==0 NorthingEnd==999999

xmlstarlet  sel -N d=http://datex2.eu/schema/1_0/1_0 -t -v 'count(//d:situation)' -n CarPark.xml

xmlstarlet  sel -N d=http://datex2.eu/schema/1_0/1_0 -t -m '//d:situation' -m 'd:situationRecord' -v 'd:nonGeneralPublicComment/d:comment/d:value' -o ' ' -v 'd:carParkOccupancy' -o ' ' -v 'd:carParkStatus' -o ' ' -v 'd:exitRate' -o ' ' -v 'd:fillRate' -o ' ' -v 'd:totalCapacity' -n CarPark.xml
```

```
<?xml version="1.0" encoding="utf-8"?>
<d2LogicalModel xmlns="http://datex2.eu/schema/1_0/1_0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" modelBaseVersion="1.0">
  <exchange>
    <supplierIdentification>
      <country>gb</country>
      <nationalIdentifier>Cambridgeshire County</nationalIdentifier>
    </supplierIdentification>
  </exchange>
  <payloadPublication xsi:type="SituationPublication" lang="en">
    <publicationTime>2019-06-11T17:29:36+01:00</publicationTime>
    <publicationCreator>
      <country>gb</country>
      <nationalIdentifier>Cambridgeshire County</nationalIdentifier>
    </publicationCreator>
    <situation id="GUID0">
      <headerInformation>
        <confidentiality>restrictedToAuthoritiesTrafficOperatorsAndPublishers</confidentiality>
        <informationUsage>broadcast</informationUsage>
        <informationStatus>real</informationStatus>
      </headerInformation>
      <situationRecord xsi:type="CarParks" id="GUIDCAMB-CP001">
        <situationRecordCreationTime>2008-11-01T16:00:00</situationRecordCreationTime>
        <situationRecordVersion>20081101160000</situationRecordVersion>
        <situationRecordVersionTime>2008-11-01T16:00:00</situationRecordVersionTime>
        <situationRecordFirstSupplierVersionTime>2008-11-01T16:00:00</situationRecordFirstSupplierVersionTime>
        <probabilityOfOccurrence>certain</probabilityOfOccurrence>
        <sourceInformation>
          <sourceName>
            <value lang="en">Cambridgeshire Government</value>
          </sourceName>
        </sourceInformation>
        <nonGeneralPublicComment>
          <comment>
            <value lang="en">Grand Arcade</value>
          </comment>
          <commentExtension>
            <nonGeneralPublicCommentExtension xmlns="">
              <shortDescription>
                <description>
                  <value lang="en">Grand Arcade</value>
                </description>
              </shortDescription>
              <modalRestrictions>
                <description>
                  <value lang="en"/>
                </description>
              </modalRestrictions>
            </nonGeneralPublicCommentExtension>
          </commentExtension>
        </nonGeneralPublicComment>
        <groupOfLocations>
          <locationContainedInGroup xsi:type="Point">
            <tpegpointLocation xsi:type="TPEGSimplePoint">
              <tpegDirection>other</tpegDirection>
              <tpegLocationType>intersection</tpegLocationType>
              <point xsi:type="TPEGJunction">
                <pointCoordinates>
                  <latitude>52.2037277</latitude>
                  <longitude>0.12105903</longitude>
                </pointCoordinates>
                <name>
                  <descriptor>
                    <value lang="en"/>
                  </descriptor>
                  <tpegDescriptorType>junctionName</tpegDescriptorType>
                </name>
                <ilc>
                  <descriptor>
                    <value lang="en"/>
                  </descriptor>
                  <tpegDescriptorType>tpegILCName1</tpegDescriptorType>
                </ilc>
              </point>
            </tpegpointLocation>
          </locationContainedInGroup>
        </groupOfLocations>
        <carParkIdentity>CAMB-CP001</carParkIdentity>
        <carParkOccupancy>484</carParkOccupancy>
        <carParkStatus>enoughSpacesAvailable</carParkStatus>
        <exitRate>0</exitRate>
        <fillRate>1</fillRate>
        <totalCapacity>890</totalCapacity>
      </situationRecord>
    </situation>
    ...
  </payloadPublication>
</d2LogicalModel>
```

</omit>

Car Park (v2.2.0)
-----------------

13 records for 'parkingAreas'/'parkingFacility' combinations, including name,
location and capacity. 13 corresponding parkingAreaStatus records, each
containing ExitRate, FillRate, Occupancy, OccupancyTrend, QueuingTime (always 0),
Reference, Status, StatusTime, numberOfVacantAssignedParkingSpaces.

Car parks are:

* Grand Arcade
* Grafton East
* Grafton West
* Park Street
* Queen Anne
* P&R Madingley Road
* P&R Trumpington
* P&R Babraham
* P&R Milton
* P&R Newmarket Rd Front
* P&R Newmarket Rd Rear
* P&R St Ives
* P&R Longstanton

<omit>

```
http --auth CambsUni:P8MSatsW9L3 get http://91.151.215.136/CloudAmber/CambsDateXII/pox/GetDateXIICarPark20 Easting==0 EastingEnd==999999 Northing==0 NorthingEnd==999999

xmlstarlet  sel -N d=http://datex2.eu/schema/2/2_0 -t -v 'count(//d:parkingArea)' -n CarPark20.xml

xmlstarlet  sel -N d=http://datex2.eu/schema/2/2_0 -t -v 'count(//d:parkingFacility)' -n CarPark20.xml

xmlstarlet  sel -N d=http://datex2.eu/schema/2/2_0 -t -v 'count(//d:parkingAreaStatus)' -n CarPark20.xml

xmlstarlet  sel -N d=http://datex2.eu/schema/2/2_0 -t -m '//d:parkingAreaStatus' -m 'd:parkingFacilityStatus' -v 'd:parkingFacilityReference/@id' -o '|' -v 'd:parkingFacilityExitRate' -o '|' -v  'd:parkingFacilityFillRate' -o '|' -v 'd:parkingFacilityOccupancy' -o '|' -v 'd:parkingFacilityOccupancyTrend' -o '|' -v 'd:parkingFacilityQueuingTime' -o '|' -v 'd:parkingFacilityStatus' -o '|' -v 'd:parkingFacilityStatusTime' -o '|' -v 'd:assignedParkingSpacesStatus/d:assignedParkingSpacesStatus/d:numberOfVacantAssignedParkingSpaces' -n CarPark20.xml
```

```
<?xml version="1.0" encoding="utf-8"?>
<d2LogicalModel xmlns="http://datex2.eu/schema/2/2_0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" modelBaseVersion="2">
  <exchange>
    <supplierIdentification>
      <country>gb</country>
      <nationalIdentifier>Cambridgeshire County</nationalIdentifier>
    </supplierIdentification>
  </exchange>
  <payloadPublication xsi:type="GenericPublication" lang="en">
    <publicationTime>2019-06-11T17:49:30.3953449+01:00</publicationTime>
    <publicationCreator>
      <country>gb</country>
      <nationalIdentifier>Cambridgeshire County</nationalIdentifier>
    </publicationCreator>
    <genericPublicationName>CarPark</genericPublicationName>
    <genericPublicationExtension>
      <parkingFacilityTablePublication>
        <headerInformation>
          <confidentiality>restrictedToAuthoritiesTrafficOperatorsAndPublishers</confidentiality>
          <informationStatus>real</informationStatus>
        </headerInformation>
        <parkingFacilityTable>
          <parkingFacilityTableVersionTime>2008-11-01T16:00:00</parkingFacilityTableVersionTime>
          <parkingArea id="CAMB-CP001" version="2.2">
            <parkingAreaName>
              <values>
                <value lang="en">Grand Arcade</value>
              </values>
            </parkingAreaName>
            <totalParkingCapacity>890</totalParkingCapacity>
            <area>
              <locationForDisplay>
                <latitude>52.2037277</latitude>
                <longitude>0.12105903</longitude>
              </locationForDisplay>
            </area>
            <parkingAreaExtension>
              <parkingAreaExtension xmlns="">
                <longDescription>
                  <description>
                    <value lang="en">Grand Arcade</value>
                  </description>
                </longDescription>
                <modalRestrictions>
                  <description>
                    <value lang="en"/>
                  </description>
                </modalRestrictions>
              </parkingAreaExtension>
            </parkingAreaExtension>
          </parkingArea>
          <parkingFacility id="CAMB-CP001" version="2.2">
            <parkingFacilityRecordVersionTime>2008-12-07T00:00:00</parkingFacilityRecordVersionTime>
            <totalParkingCapacity>890</totalParkingCapacity>
            <facilityLocation xsi:type="Area">
              <locationForDisplay>
                <latitude>52.2037277</latitude>
                <longitude>0.12105903</longitude>
              </locationForDisplay>
            </facilityLocation>
            <parkingFacilityConfiguration>
              <almostFullDecreasing>770</almostFullDecreasing>
              <almostFullIncreasing>800</almostFullIncreasing>
              <entranceFull>889</entranceFull>
              <fullDecreasing>840</fullDecreasing>
              <fullIncreasing>889</fullIncreasing>
            </parkingFacilityConfiguration>
          </parkingFacility>
        </parkingFacilityTable>
        ...
      </parkingFacilityTablePublication>
      <parkingFacilityTableStatusPublication>
        <headerInformation>
          <areaOfInterest>national</areaOfInterest>
          <confidentiality>restrictedToAuthoritiesTrafficOperatorsAndPublishers</confidentiality>
          <informationStatus>real</informationStatus>
        </headerInformation>
        <parkingAreaStatus>
          <parkingAreaReference id="CAMB-CP001" version="2.2" targetClass="ParkingArea"/>
          <parkingFacilityStatus>
            <parkingFacilityExitRate>3</parkingFacilityExitRate>
            <parkingFacilityFillRate>0</parkingFacilityFillRate>
            <parkingFacilityOccupancy>476</parkingFacilityOccupancy>
            <parkingFacilityOccupancyTrend>decreasing</parkingFacilityOccupancyTrend>
            <parkingFacilityQueuingTime>0</parkingFacilityQueuingTime>
            <parkingFacilityReference id="CAMB-CP001" version="2.2" targetClass="ParkingFacility"/>
            <parkingFacilityStatus>open</parkingFacilityStatus>
            <parkingFacilityStatusTime>2019-06-11T17:48:01</parkingFacilityStatusTime>
            <assignedParkingSpacesStatus index="0">
              <assignedParkingSpacesStatus>
                <numberOfVacantAssignedParkingSpaces>414</numberOfVacantAssignedParkingSpaces>
              </assignedParkingSpacesStatus>
            </assignedParkingSpacesStatus>
          </parkingFacilityStatus>
        </parkingAreaStatus>
        ...
      </parkingFacilityTableStatusPublication>
    </genericPublicationExtension>
  </payloadPublication>
</d2LogicalModel>
```

</omit>

CCTV
----

437 records giving a location (by reference).
No obvious validity information, but the records have creation timestamps
between 2011-02 and 2018-09, and 389 records have a field 'inhibit' set to 'true'
(the meaning of which is unknown).

<omit>

```
http --auth CambsUni:P8MSatsW9L3 get http://91.151.215.136/CloudAmber/CambsDateXII/pox/GetDateXIICCTV Easting==0 EastingEnd==999999 Northing==0 NorthingEnd==999999

xmlstarlet sel -N d=http://datex2.eu/schema/1_0/1_0 -t -v 'count(//situationRecord)' -n CCTV.xml

xmlstarlet sel -N d=http://datex2.eu/schema/1_0/1_0 -t -m '//situationRecord' -v 'situationRecordCreationTime' -o '|' -v 'inhibit' -n CCTV.xml

xmlstarlet sel -N d=http://datex2.eu/schema/1_0/1_0 -t -m '//situationRecord' -v 'count(inhibit["true"])' -n CCTV.xml

xmlstarlet sel -N d=http://datex2.eu/schema/1_0/1_0 -t -v 'count(//situationRecord[inhibit = "false"])' -n CCTV.xml
```

```
<?xml version="1.0" encoding="utf-8"?>
<d2LogicalModel xmlns="http://datex2.eu/schema/1_0/1_0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" modelBaseVersion="1.0">
  <exchange>
    <supplierIdentification>
      <country>gb</country>
      <nationalIdentifier>Cambridgeshire County</nationalIdentifier>
    </supplierIdentification>
  </exchange>
  <d2LogicalModelExtension>
    <SituationPublication xmlns="" lang="en">
      <publicationTime>2019-06-11T17:54:44.1780469+01:00</publicationTime>
      <publicationCreator>
        <country>gb</country>
        <nationalIdentifier>Cambridgeshire County</nationalIdentifier>
      </publicationCreator>
      <situation id="GUID0">
        <headerInformation>
          <confidentiality>restrictedToAuthoritiesTrafficOperatorsAndPublishers</confidentiality>
          <informationUsage>broadcast</informationUsage>
          <informationStatus>real</informationStatus>
        </headerInformation>
        <situationRecord id="GUIDCAMB-172.16.0.189">
          <situationRecordCreationTime>2011-10-14T14:00:00</situationRecordCreationTime>
          <situationRecordVersion>00010101000000</situationRecordVersion>
          <situationRecordVersionTime>0001-01-01T00:00:00</situationRecordVersionTime>
          <situationRecordFirstSupplierVersionTime>2011-10-14T14:00:00</situationRecordFirstSupplierVersionTime>
          <probabilityOfOccurrence>certain</probabilityOfOccurrence>
          <sourceInformation>
            <sourceName>
              <value lang="en">Cambridgeshire Government</value>
            </sourceName>
          </sourceInformation>
          <groupOfLocations>
            <locationContainedInGroup>
              <predefinedLocationReference>CCTVCAMB-172.16.0.189</predefinedLocationReference>
            </locationContainedInGroup>
          </groupOfLocations>
          <inhibit>true</inhibit>
        </situationRecord>
      </situation>
      ...
    </SituationPublication>
  </d2LogicalModelExtension>
</d2LogicalModel>
```
</omit>

Predefined Location
-------------------

Records containing identifiers, names (sometimes), descriptions and positions for various types of
location:

* Traffic Data Links: 114 linear features (probably relating to the TrafficData feed)
* Traffic Data Section: 800 linear features (probably also relating to the TrafficData feed)
* VMS: 182 positions ('Cambridgeshire Locations', probably relating to the AllVMS feed)
  Also contains 'numberOfCharacters', 'numberOfRows', 'vmsType'
* Matrix: feed is empty
* Journey Time Sections: 114 linear features. Identical data to that served under 'Traffic Data Links'
* CCTV: 874 positions ('Cambridgeshire CCTV Locations', probably relating to the CCTV feed).
  Also contains 'cctvUri' with values of the form `http://www.cambsvoyager.com/cctvimage/CAMB-52538` though none seem to work

<omit>

e.g. type=link, section, vms, matrix, tr, cctv

```
http --auth CambsUni:P8MSatsW9L3 get http://91.151.215.136/CloudAmber/CambsDateXII/pox/GetDateXIIPredefinedLocation type==link

xmlstarlet sel -N d=http://datex2.eu/schema/1_0/1_0 -t -v 'count(//d:predefinedLocation)' -n PrdefinedLocation-link.xml

sel -N d=http://datex2.eu/schema/1_0/1_0 -t -v 'count(//d:predefinedLocation)' -n PrdefinedLocation-section.xml

xmlstarlet sel -N d=http://datex2.eu/schema/1_0/1_0 -t -v 'count(//d:predefinedLocation)' -n PrdefinedLocation-vms.xml

xmlstarlet sel -N d=http://datex2.eu/schema/1_0/1_0 -t -v 'count(//d:predefinedLocation)' -n PrdefinedLocation-matrix.xml

xmlstarlet sel -N d=http://datex2.eu/schema/1_0/1_0 -t -v 'count(//d:predefinedLocation)' -n PrdefinedLocation-cctv.xml
```

```
<?xml version="1.0" encoding="utf-8"?>
<d2LogicalModel xmlns="http://datex2.eu/schema/1_0/1_0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" modelBaseVersion="1.0">
  <exchange>
    <supplierIdentification>
      <country>gb</country>
      <nationalIdentifier>Cambridgeshire County</nationalIdentifier>
    </supplierIdentification>
  </exchange>
  <payloadPublication xsi:type="PredefinedLocationsPublication" lang="en">
    <publicationTime>2019-06-11T17:29:08+01:00</publicationTime>
    <publicationCreator>
      <country>gb</country>
      <nationalIdentifier>Cambridgeshire County</nationalIdentifier>
    </publicationCreator>
    <headerInformation>
      <confidentiality>restrictedToAuthoritiesTrafficOperatorsAndPublishers</confidentiality>
      <informationUsage>broadcast</informationUsage>
      <informationStatus>real</informationStatus>
    </headerInformation>
    <predefinedLocationSet id="GUID-Cambridgeshire-Link-Locations">
      <predefinedLocation id="LINKCAMB-1454085853">
        <predefinedLocationName>
          <value lang="en"/>
        </predefinedLocationName>
        <predefinedLocation xsi:type="Linear">
          <tpeglinearLocation>
            <tpegDirection>other</tpegDirection>
            <tpegLocationType>segment</tpegLocationType>
            <to xsi:type="TPEGJunction">
              <pointCoordinates>
                <latitude>52.2008247</latitude>
                <longitude>0.101223484</longitude>
              </pointCoordinates>
              <name>
                <descriptor>
                  <value lang="en"/>
                </descriptor>
                <tpegDescriptorType>junctionName</tpegDescriptorType>
              </name>
              <ilc>
                <descriptor>
                  <value lang="en"/>
                </descriptor>
                <tpegDescriptorType>tpegILCName1</tpegDescriptorType>
              </ilc>
            </to>
            <from xsi:type="TPEGJunction">
              <pointCoordinates>
                <latitude>52.2008247</latitude>
                <longitude>0.101223484</longitude>
              </pointCoordinates>
              <name>
                <descriptor>
                  <value lang="en"/>
                </descriptor>
                <tpegDescriptorType>junctionName</tpegDescriptorType>
              </name>
              <ilc>
                <descriptor>
                  <value lang="en"/>
                </descriptor>
                <tpegDescriptorType>tpegILCName1</tpegDescriptorType>
              </ilc>
            </from>
          </tpeglinearLocation>
        </predefinedLocation>
        ...
      </predefinedLocationSet>
  </payloadPublication>
</d2LogicalModel>
```

</omit>