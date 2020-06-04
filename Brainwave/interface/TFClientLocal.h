#ifndef SonicCMS_TensorRT_TFClientLocal
#define SonicCMS_TensorRT_TFClientLocal

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "SonicCMS/Core/interface/SonicClientSync.h"

#include <string>
#include <vector>
#include <memory>

#include "tensorflow/core/framework/tensor.h"
#include "tensorflow/core/graph/default_device.h"
#include "tensorflow/core/public/session.h"
namespace edm {
	class ParameterSetDescription;
}
class TFClientLocal : public SonicClientSync<tensorflow::Tensor> {
	public:
		//constructor
		TFClientLocal(const edm::ParameterSet& params);
		//destructor
		~TFClientLocal();
		unsigned ninput() const { return ninput_; }
		unsigned noutput() const { return noutput_; }
		unsigned batchSize() const { return batchSize_; }
		static void fillPSetDescription(edm::ParameterSetDescription& iDesc);
	protected:
		void predictImpl() override;

		void loadModel(const std::string& classifier_file);
		void createSessions();
		std::vector<tensorflow::Tensor> runFeaturizer(const tensorflow::Tensor& inputImage) const;
		std::vector<tensorflow::Tensor> runClassifier(const tensorflow::Tensor& inputClassifier) const;
		tensorflow::Tensor createFeatureList(const tensorflow::Tensor& input) const;


		//members
		tensorflow::GraphDef* graphDefFeaturizer_ = nullptr;
		tensorflow::GraphDef* graphDefClassifier_ = nullptr;
		tensorflow::Session* sessionF_ = nullptr;
		tensorflow::Session* sessionC_ = nullptr;
		unsigned batchSize_;
		unsigned ninput_;
		unsigned noutput_;
};

#endif

