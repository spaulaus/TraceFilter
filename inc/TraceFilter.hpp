/***************************************************************************
  *  Copyright S. V. Paulauskas 2014                                       *
  *                                                                        *
  *  This program is free software: you can redistribute it and/or modify  *
  *  it under the terms of the GNU General Public License as published by  *
  *  the Free Software Foundation, version 3.0 License.                    *
  *                                                                        *
  *  This program is distributed in the hope that it will be useful,       *
  *  but WITHOUT ANY WARRANTY; without even the implied warranty of        *
  *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
  *  GNU General Public License for more details.                          *
  *                                                                        *
  *  You should have received a copy of the GNU General Public License     *
  *  along with this program.  If not, see <http://www.gnu.org/licenses/>. *
  **************************************************************************
*/
/** \file TraceFilter.hpp
 *  \brief A class to perform trapezoidal filtering
 *  \author S. V. Paulauskas
 *  \date 23 April 2014
 *
 *  This code is based off of the IGOR macro energy.ipf
 *  written by H. Tan of XIA LLC and parts of the nscope
 *  program written at the NSCL written by C.Prokop.
 *
 */
#ifndef __TRACEFILTER_HPP__
#define __TRACEFILTER_HPP__
#include <vector>
#include <utility>

/*! The class to hold the Filter parameters */
class FilterParameters {
public:
    FilterParameters(){};
    FilterParameters(const double &l, const double &g, const double &tau);
    FilterParameters(const double &l, const double &g, const unsigned int &thresh);
    ~FilterParameters(){};

    double GetFlattop(void){return(g_);};
    double GetRisetime(void){return(l_);};
    double GetTau(void){return(tau_);};
    double GetThreshold(void){return(thresh_);};

    void SetFlattop(const double &a){g_ = a;};
    void SetRisetime(const double &a){l_ = a;};
    void SetTau(const double &a){tau_ = a;};
    void SetThreshold(const double &a){thresh_ = a;};
private:
    double g_, l_, tau_, tau1_, tau_2, thresh_;
};

/*! The class to perform the filtering */
class TraceFilter {
public:
    TraceFilter(){};
    TraceFilter(const int &adcSample){adc_ = adcSample;};
    TraceFilter(const unsigned int &adc, 
                const FilterParameters &tFilt, const FilterParameters &eFilt);
    ~TraceFilter(){};

    double GetAdcSample(void){return(adc_);};
    double GetBaseline(void){return(baseline_);};
    double GetEnergy(void){return(energy_);};
    unsigned int GetTriggerPosition(void){return(trigPos_);};
    std::vector<double> GetTriggerFilter(void) {return(trigFilter_);};
    std::vector<double> GetEnergyFilterCoefficients(void) {return(coeffs_);};
    std::vector<unsigned int> GetEnergySumLimits(void){return(limits_);};

    void CalcFilters(const std::vector<double> *sig);
    
    void SetAdcSample(const double &a){adc_ = a;};
    void SetSig(const std::vector<double> *sig){sig_ = sig;};
    void SetVerbose(const bool &a){loud_ = a;};
private:
    bool loud_, finishedConvert_;
    unsigned int adc_, trigPos_;
    double baseline_, energy_;

    FilterParameters e_, t_;
    
    const std::vector<double> *sig_;
    std::vector<double> coeffs_, trigFilter_;
    std::vector<unsigned int> limits_;
    
    bool CalcBaseline(void); 
    bool CalcEnergyFilterLimits(void);
    bool CalcTriggerFilter(void);

    void CalcEnergyFilterCoeffs(void);
    void CalcEnergyFilter(void);
    void ConvertToClockticks(void);
};
#endif //__TRACEFILTER_HPP__
