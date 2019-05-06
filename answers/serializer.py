import json
from rest_framework import serializers
from answers.models import Answers


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = '__all__'


CONST_NUMBER_COMPARE = 'number_compare'
CONST_YESNO_COMPARE = 'yesno_compare'
CONST_GENDER_COMPARE = 'gender_compare'
MULTY_OR_COMPARE = 'multy_or_compare'
MULTY_AND_COMAPRE = 'multy_and_compare'


class AskSerializer(serializers.Serializer):
    gender = serializers.CharField(required=True,
                                   allow_null=False)

    age = serializers.IntegerField(required=True,
                                   allow_null=False)

    abdominal_pain = serializers.CharField(required=True,
                                           allow_null=False)

    systolic_bp = serializers.IntegerField(required=True,
                                           allow_null=False)

    diastolic_bp = serializers.IntegerField(required=True,
                                            allow_null=False)

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        # get all answers from data base
        answers = Answers.objects.all()
        self.validated_data['response'] = []

        # check single rule from answer
        for answer in answers:
            # get rule
            rule = answer.rule
            # string rule from data base to json
            json_rule = json.loads(rule)

            compare_data = self.compare_number(json_rule, validated_data, answer)
            if compare_data:
                self.validated_data['response'].append(compare_data)

            compare_yesno_data = self.compare_yes_no(json_rule, validated_data, answer)
            if compare_yesno_data:
                self.validated_data['response'].append(compare_yesno_data)

            compare_gender_data = self.compare_gender(json_rule, validated_data, answer)
            if compare_gender_data:
                self.validated_data['response'].append(compare_gender_data)

            multy_compare_data = self.multy_or_compare(json_rule, validated_data, answer)
            if multy_compare_data:
                self.validated_data['response'].append(multy_compare_data)

            multy_and_compare_data = self.multy_and_compare(json_rule, validated_data, answer)
            if multy_and_compare_data:
                self.validated_data['response'].append(multy_and_compare_data)

        return self.validated_data

    def compare_number(self, json_rule, validated_data, answer):
        if json_rule['type'] in CONST_NUMBER_COMPARE:
            if ">" in json_rule['operand']:
                data = self.single_compare_more(validated_data,
                                                json_rule,
                                                answer)
                if data:
                    return data

            elif "<" in json_rule['operand']:
                data = self.single_compare_less(validated_data,
                                                json_rule,
                                                answer)
                if data:
                    return data

            elif "==" in json_rule['operand']:
                data = self.single_compare_eqals(validated_data,
                                                 json_rule,
                                                 answer)
                if data:
                    return data

    def compare_gender(self, json_rule, validated_data, answer):
        if json_rule['type'] in CONST_GENDER_COMPARE:
            data = self.logic_compare(validated_data,
                                      json_rule,
                                      answer)
            if data:
                return data

    def compare_yes_no(self, json_rule, validated_data, answer):
        if json_rule['type'] in CONST_YESNO_COMPARE:
            data = self.logic_compare(validated_data,
                                      json_rule,
                                      answer)
            if data:
                return data

    def multy_or_compare(self, json_rule, validated_data, answer):
        if json_rule['type'] in MULTY_OR_COMPARE:
            for multy_rulles in json_rule['rules']:
                compare_data = self.compare_number(multy_rulles, validated_data, answer)
                if compare_data:
                    return compare_data

                compare_data_yesno = self.compare_yes_no(multy_rulles, validated_data, answer)
                if compare_data_yesno:
                    return compare_data_yesno

                compare_data_gender = self.compare_gender(multy_rulles, validated_data, answer)
                if compare_data_gender:
                    return compare_data_gender

    def multy_and_compare(self, json_rule, validated_data, answer):
        if json_rule['type'] in MULTY_AND_COMAPRE:
            count_rules = len(json_rule['rules'])
            array = []
            for multy_rulles in json_rule['rules']:
                compare_data = self.compare_number(multy_rulles, validated_data, answer)
                if compare_data:
                    array.append(compare_data)

                compare_data_yesno = self.compare_yes_no(multy_rulles, validated_data, answer)
                if compare_data_yesno:
                    array.append(compare_data_yesno)

                compare_data_gender = self.compare_gender(multy_rulles, validated_data, answer)
                if compare_data_gender:
                    array.append(compare_data_gender)

            if len(array) == count_rules:
                data = {'id': answer.pk, 'answer': answer.positive_answer}
                return data
            else:
                return None

    def logic_compare(self, validated_data, json_rule, answer):
        if validated_data[json_rule['field_name']] == json_rule['operand']:
            data = {'id': answer.pk, 'answer': answer.positive_answer}
            return data

    def single_compare_more(self, validated_data, json_rule, answer):
        if validated_data[json_rule['field_name']] > json_rule['number_rule']:
            data = {'id': answer.pk, 'answer': answer.positive_answer}
            return data

    def single_compare_less(self, validated_data, json_rule, answer):
        if validated_data[json_rule['field_name']] < json_rule['number_rule']:
            data = {'id': answer.pk, 'answer': answer.positive_answer}
            return data

    def single_compare_eqals(self, validated_data, json_rule, answer):
        if validated_data[json_rule['field_name']] == json_rule['number_rule']:
            data = {'id': answer.pk, 'answer': answer.positive_answer}
            return data
