#ifndef SonicCMS_Core_SonicEDProducer
#define SonicCMS_Core_SonicEDProducer

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Concurrency/interface/WaitingTaskWithArenaHolder.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include <sstream>
#include <string>
#include <chrono>
#include <fstream>

//this is a stream producer because client operations are not multithread-safe in general
//it is designed such that the user never has to interact with the client or the acquire() callback directly
template <typename Client, typename... Capabilities>
class SonicEDProducer : public edm::stream::EDProducer<edm::ExternalWork, Capabilities...> {
	public:
		//typedefs to simplify usage
		typedef typename Client::Input Input;
		typedef typename Client::Output Output;
		//constructor
		SonicEDProducer(edm::ParameterSet const& cfg) : client_(cfg.getParameter<edm::ParameterSet>("Client")) {
            sumLoadTime = 0;
            numLoadTime = 0;
        }

		//destructor
		~SonicEDProducer() {
            /*
            std::stringstream msg;
            msg << "Produced by SonicEDProducer" << std::endl;
            if (numLoadTime == 0) {
                msg << "numLoadTime was 0." << std::endl;
            }
            else {
                msg << "Load time: " << float(sumLoadTime) / numLoadTime << std::endl;
            }

            writeData(&msg);

            std::ofstream file("./data/producer-data.dat");
            file << msg.str();
            file.close();*/
        }
		
		//derived classes use a dedicated acquire() interface that incorporates client_.input()
		//(no need to interact with callback holder)
		void acquire(edm::Event const& iEvent, edm::EventSetup const& iSetup, edm::WaitingTaskWithArenaHolder holder) override final {
			auto t0 = std::chrono::high_resolution_clock::now();
			acquire(iEvent, iSetup, client_.input());
			auto t1 = std::chrono::high_resolution_clock::now();
			if(!debugName_.empty()) {
               sumLoadTime += (unsigned int)std::chrono::duration_cast<std::chrono::microseconds>(t1 - t0).count();
               numLoadTime++;
            }
			client_.predict(holder);
		}
		virtual void acquire(edm::Event const& iEvent, edm::EventSetup const& iSetup, Input& iInput) = 0;
		//derived classes use a dedicated produce() interface that incorporates client_.output()
		void produce(edm::Event& iEvent, edm::EventSetup const& iSetup) override final {
			//todo: measure time between acquire and produce
			produce(iEvent, iSetup, client_.output());
		}
		virtual void produce(edm::Event& iEvent, edm::EventSetup const& iSetup, Output const& iOutput) = 0;
		
	protected:
		//for debugging
		void setDebugName(const std::string& debugName){
			debugName_ = debugName;
			client_.setDebugName(debugName);
		}
		//members
		Client client_;
		std::string debugName_;

    private:
        virtual void writeData(std::stringstream* msg) {}
        unsigned int sumLoadTime;
        unsigned int numLoadTime;
};

#endif

