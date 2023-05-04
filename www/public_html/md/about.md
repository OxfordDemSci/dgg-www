<h5 class="fw-bold">Using Digital Traces to Measure Digital Gender Inequality in Real-Time</h5>
<p>
The tremendous expansion of information and communication technologies (ICTs) has transformed the ways in which 
individuals seek information, communicate and participate in their communities. Participating in the digital revolution 
is more important than ever across different spheres of life. Despite the rapid expansion of ICTs worldwide, women lag 
behind men in access and use of the internet and mobile phones in many parts of the world, particularly in 
low- and middle-income countries <a href="https://www.itu.int/en/ITU-D/Statistics/Documents/facts/ICTFactsFigures2017.pdf" target="_blank">(ITU 2017)</a>.
</p>

<p>
Gender equality in internet and mobile phone access, and improving digital literacy are important targets
<a href="https://sustainabledevelopment.un.org/content/documents/10789Chapter3_GSDR2016.pdf" target="_blank">(UN 2016)</a> 
within the United Nations’ (UN) Sustainable Development Goals (SDGs). Acknowledging the tremendous and wide-ranging 
potential of these technologies, the UN SDG 5 to achieve gender equality pledges to “enhance the use of…information and 
communication technology to promote the empowerment of women” (Goal 5b). In March 2013, the International 
Telecommunications Union (ITU) and the United Nations Educational, Scientific and Cultural Organization (UNESCO) 
Broadband Commission for Digital Development
<a href="https://www.broadbandcommission.org/Pages/default.aspx" target="_blank">(ITU & UNESCO 2022)</a> 
further endorsed a target calling for gender equality in access to broadband by 2020 
<a href="https://es.unesco.org/node/83355" target="_blank">(UNESCO 2013)</a>.
</p>

<p>
Tracking progress on gender inequalities in internet and mobile access and use – digital gender gaps – is very 
important to ensure that women benefit from the opportunities afforded by the digital revolution
<a href="https://broadbandcommission.org/Documents/publications/DigitalGenderDivideProgressReport2018.pdf" target="_blank">(ITU 2018)</a>. 
But measuring and sizing this gender gap has proven to be challenging due to significant gender data gaps 
<a href="https://www.data2x.org/what-is-gender-data/gender-data-gaps/" target="_blank">(Data2X 2022)</a>. 
There are limited data from surveys or population-level data sources that examine digital inequalities.
</p>

<p>
How can we better measure digital gender gaps in real-time? In which countries are women most “invisible” online and not 
participating equally in the digital revolution?
</p>

<p>
With support from the Bill and Melinda Gates Foundation, the project “Mapping global gender gaps in digital connectivity” 
based at the University of Oxford and collaborating with Saarland University's Societal Computing Department has been 
exploring how big data innovations can help us measure women’s participation in the digital revolution in real-time. 
</p>


<hr>

<h5 class="fw-bold"> Digital Gender Gap Indicators</h5>

<p>
Our approach leverages online digital trace data from the Facebook Marketing Application Programming Interface (API) in 
combination with different development indicators from sources such as the World Bank and the United Nations (UN) to 
estimate global digital gender gaps (GG) in internet and mobile phone use. The full details of the data and methods 
used to generate the estimates shown in the maps on this website are described in "Using Facebook ad data to track the 
global digital gender gap" 
<a href="https://doi.org/10.1016/j.worlddev.2018.03.007" target="_blank">(Fatehkia et al. 2018)</a>.
</p>

<p>
We provide estimates of two measures – 1) Internet Gender Gap, 2) Mobile Gender Gap. Both measures are female-to-male 
ratios of gender-specific internet penetration, and lie in the range of 0 to 1. Values of 1 or close to 1 show that 
the gender gap has closed. For example, a value of 0.75 could be interpreted as a 25% gap between male and female 
internet use, with 75 women online for roughly 100 men who are.
</p>

<p>
For each measure – Internet GG and Mobile Phone GG – we provide three estimates.
</p>


<h5 class="fw-bold"> Internet Gender Gaps</h5>
<p>
The <strong>Internet GG - ITU</strong> shows the ratio of female-to-male internet use from International Telecommunication Union 
(ITU) statistics. These are available for the fewest countries and are infrequently updated depending on when the survey 
for a given year was last collected.
</p>

<p>
The <strong>Internet GG – Online</strong> shows the ratio of female-to-male internet use estimated using the Facebook Gender Gap 
Index (see below for more information) by country. These estimates are available for the largest number of countries 
and are available with monthly frequency.
</p>

<p>
The <strong>Internet GG – Combined</strong> shows the ratio of female-to-male internet use estimated using the Facebook Gender Gap 
Index by country combined with other offline indicators on the country’s development status such as its Human 
Development Index. This model is our best-performing model in terms of its fit with ITU statistics, and these 
estimates are available for more countries than ITU statistics. Their geographical coverage is not as wide as that of 
the Online Model Prediction and the underlying information used to generate these predictions is only annually updated.
</p>

<p>
The <strong>Internet GG – Offline</strong> shows the ratio of female-to-male internet use estimated using only offline indicators 
on the country’s development status such as its Human Development Index. Estimates from these models have the worst 
fit with ITU statistics on the internet GG, and the underlying data used to generate these are updated with an annual 
or longer frequency.
</p>

<h5 class="fw-bold"> Mobile Gender Gaps</h5>
<p>
The <strong>Mobile GG – GSMA</strong> shows the ratio of female-to-male mobile phone use from published Global System for Mobile 
Communications Association (GSMA) reports. These are available for the fewest countries and are infrequently updated.
</p>

<p>
The <strong>Mobile GG – Online</strong> shows the ratio of female-to-male mobile phone use estimated using the Facebook Gender Gap Index 
(see below for more information) by country. These estimates are available for the largest number of countries and are 
available with monthly frequency, although their fit with GSMA statistics is worse than the other two models.
</p>

<p>
The <strong>Mobile GG – Combined</strong> shows the ratio of female-to-male mobile phone use estimated using the Facebook Gender Gap 
Index by country combined with other indicators on the country’s development status such as its Human Development 
Index. Estimates from these models are closer to GSMA statistics on the mobile GG, and available for more countries 
than GSMA statistics, but not as many as those from the Online Model Prediction.
</p>

<p>
The <strong>Mobile GG – Offline</strong> shows the ratio of female-to-male mobile phone use estimated using only offline indicators on 
the country’s development status such as its Human Development Index. The underlying data used to generate these are 
updated with an annual or longer frequency.
</p>


<hr>

<h5 class="fw-bold"> Data Informing our Estimates</h5>
<h5 class="fw-bold"> Facebook Gender Gap Index</h5>
<p>
We collect data for countries globally on the aggregate numbers of monthly active female and male users of Facebook 
available through the marketing API. Using these aggregate numbers, we generate the “Facebook Gender Gap Index”, an 
indicator of the number of female-to-male Facebook users in a country. We compute this index monthly. While the Facebook 
Gender Gap Index reflects gender gaps in who has Facebook accounts and not internet use per se, we have found the 
Facebook Gender Gap Index is highly correlated with statistics on internet (from the ITU) and mobile phone gender gaps 
(from the GSMA) collected via surveys, for the countries for which these data are available.
</p>

<p>
Looking at statistics of gender gaps in Facebook users can help us predict gender gaps in internet use, but as data 
on Facebook users are available for many more countries than statistics from the ITU, we can expand geographical 
coverage of this indicator by using the online data. Our modelled predictions of the internet ad mobile gender gaps, 
derived from Facebook data, are the ones shown on the platform as the online or combined indicators.
</p>

<h5 class="fw-bold"> Offline Indicators</h5>
</p>
Our dataset uses a number of country-level development indicators (e.g Human Development Index, Gross Domestic 
Product (GDP) per capita) and global gender gap indicators in other domains (e.g literacy). For more information 
see our paper and related publications (see below).
</p>


<hr>

<h5 class="fw-bold"> Funding</h5>
<p>We are grateful to funding from the Bill and Melinda Gates Foundation (INV-045370), Economic and Social Research Council 
(ESRC) Impact Acceleration Account (IAA) (2021-22), and to Data2X (2017-2020).</p>


<h5 class="fw-bold"> Suggested Citation</h5>
<p>When using the data, please acknowledge our website (digitalgendergaps.org), cite its source code (Leasure et al 2023) 
and/or cite our related academic publications, as appropriate.</p>

<ul style="list-style: circle;">
<li style="margin:0 0 10px 0;">
    Fatehkia M, Kashyap R, Weber I. 2018. Using Facebook ad data to track the global digital gender gap. <i>World 
    Development</i> 107:189-209. 
    <a href="https://doi.org/10.1016/j.worlddev.2018.03.007" target="_blank">https://doi.org/10.1016/j.worlddev.2018.03.007</a> 
</li>
<li style="margin:0 0 10px 0;">
    Kashyap R, Fatehkia M, Al Tamime R, Weber I. 2020. Monitoring global digital gender inequality using the online 
    populations of Facebook and Google. <i>Demographic Research</i> 43: 779-816. 
    <a href="https://www.jstor.org/stable/26967824" target="_blank">https://www.jstor.org/stable/26967824</a>
</li>
<li style="margin:0 0 10px 0;">
    Leasure DR, Yan J, Bondarenko M, Kerr D, Fatehkia M, Weber I, Kashyap R. 2023. Digital Gender Gaps Web Application. 
    <i>Zenodo, GitHub</i>. doi:<a href="https://doi.org/10.5281/zenodo.7897491" target="_blank">10.5281/zenodo.7897491</a>. 
    <a href="https://github.com/OxfordDemSci/dgg-www" target="_blank">https://github.com/OxfordDemSci/dgg-www</a>.
</li>
<li style="margin:0 0 10px 0;">
    Weber I, Kashyap R, Zagheni E. 2018. Using advertising audience estimates to improve global development statistics. 
    <i>ITU Journal: ICT Discoveries</i> 1(2). 
    <a href="https://ora.ox.ac.uk/objects/uuid:991b732a-2537-40ab-b045-1110fb175fac" target="_blank">https://ora.ox.ac.uk/objects/uuid:991b732a-2537-40ab-b045-1110fb175fac</a> 
</li>
</ul>


<h5 class="fw-bold"> Source Code</h5>
<p>
The source code for this web application is openly available from 
<a href="https://github.com/OxfordDemSci/dgg-www" target="_blank">OxfordDemSci on GitHub</a>.
</p>


<h5 class="fw-bold"> Data license</h5>
<p>
You are free to share and adapt data accessed through this website under the terms of a 
<a href="https://creativecommons.org/licenses/by/4.0/" target="_blank">CC-BY 4.0 license</a>. 
You must give appropriate credit, provide a link to the license, and indicate if changes were made. 
</p>


<h5 class="fw-bold"> Automated Data Requests via API</h5>
<p>
You can access all data displayed in this website through our API (Application Programming Interface). The API
and its documentation are available from <a href="./api/v1">https://digitalgendergaps.org/api/v1 </a>. 
This provides a way to rapidly retrieve data for individual countries, specific dates, or bulk downloads. We aim to 
update our data once per month, and we will always make our most recent results openly available free of charge. You 
can also use our API to develop your own web applications (like this one) that query our database through the API 
on-the-fly based on user-defined settings.
</p>




<hr>

<h5 class="fw-bold">Privacy Policy</h5>

<h5 class="fw-bold">Cookies</h5>
<p>No data is stored in cookies, or other forms of browser storage.</p>


<h5 class="fw-bold">Embedded content from other websites</h5>
<p>Our site has no embedded content so other sites should not be able to track your visit here.</p>

<h5 class="fw-bold">Analytics</h5>
<p>
Our CDN (Cloudfront) records aggregate visitor stats to our site that includes visitor characteristics, these are 
provided to us in aggregate form. Our CDN is not authorised by us to process any other data, or store any personal data 
after it has been processed into aggregate statistics.
</p>

<h5 class="fw-bold">Facebook advertising data</h5>
<p>
We collect aggregate, anonymous counts of Facebook users from the Facebook Marketing API. We receive only aggregate 
counts of users, and we do not process or store any individual user identifiers..
</p>
<p>
This data is then processed and combined with other data and used as inputs in our prediction models to generate the 
gender gap estimates presented. 
</p>


<h5 class="fw-bold">Who we share your data with</h5>
<p>
No personal data is collected or shared by us.
</p>


<h5 class="fw-bold">What rights you have over your data</h5>
<p>
If we held any of your personal data, you could request to receive an exported file of the personal data we hold about 
you, including any data you have provided to us. You could also request that we erase any personal data we hold about 
you. This would not include any data we are obliged to keep for administrative, legal, or security purposes.
</p>


<h5 class="fw-bold">Data license</h5>
<p>
All visualisations and digital gender gap estimates generated as a part of the project are shared freely under the terms 
of a 
<a href="https://creativecommons.org/licenses/by/4.0/" target="_blank">CC-BY 4.0 license</a>.
</p>

<h5 class="fw-bold">Our contact information</h5>
<p>
Contact us at <a href="(mailto:ridhi.kashyap@nuffield.ox.ac.uk">ridhi.kashyap@nuffield.ox.ac.uk</a> if you have any 
questions, concerns or data enquiries.
</p>

