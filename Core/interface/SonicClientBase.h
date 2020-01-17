#ifndef SonicCMS_Core_SonicClientBase
#define SonicCMS_Core_SonicClientBase

#include "FWCore/Concurrency/interface/WaitingTaskWithArenaHolder.h"

#include <string>
#include <chrono>
#include <exception>

class SonicClientBase {
	public:
		//destructor
		virtual ~SonicClientBase() {}

		void setDebugName(const std::string& debugName) { debugName_ = debugName; }

		//main operation
		virtual void predict(edm::WaitingTaskWithArenaHolder holder) = 0;

	protected:
		virtual void predictImpl() = 0;

		void setStartTime() {
			if(debugName_.empty()) return;
			t0_ = std::chrono::high_resolution_clock::now();
			setTime_ = true;
		}

		void finish(std::exception_ptr eptr = std::exception_ptr{}) {
            /*unsigned int clientTime = 0;
			if(setTime_){
				auto t1 = std::chrono::high_resolution_clock::now();
				clientTime = (unsigned int)std::chrono::duration_cast<std::chrono::microseconds>(t1 - t0_).count();
			}*/
			holder_.doneWaiting(eptr);
		}

		//members
		edm::WaitingTaskWithArenaHolder holder_;

		//for logging/debugging
		std::string debugName_;
		std::chrono::time_point<std::chrono::high_resolution_clock> t0_;
		bool setTime_ = false;
};

#endif
