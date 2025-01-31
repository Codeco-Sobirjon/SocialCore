from rest_framework import serializers
from apps.accounts.serializers import CustomUserDetailSerializer
from apps.chat.models import Conversation, Message
from apps.chat.utils import custom_user_has_student_role, custom_user_has_author_role


class MessageSerializer(serializers.ModelSerializer):
    sender = CustomUserDetailSerializer()
    sender_type = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'text', 'sender_type', 'timestamp']

    def get_sender_type(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return None

        current_user = request.user
        conversation = obj.conversation_id

        if conversation.initiator == current_user:
            return "initiator" if obj.sender == current_user else "receiver"
        elif conversation.receiver == current_user:
            return "initiator" if obj.sender == current_user else "receiver"

        else:
            return None


class MessageListSerializer(serializers.ModelSerializer):
    sender_type = serializers.SerializerMethodField()

    class Meta:
        model = Message
        exclude = ('conversation_id',)

    def get_sender_type(self, obj):
        current_user = self.context.get('request')
        if not current_user or not current_user.is_authenticated:
            return None

        conversation = obj.conversation_id

        if conversation.initiator == current_user:

            return "initiator" if obj.sender == current_user else "receiver"
        elif conversation.receiver == current_user:

            return "initiator" if obj.sender == current_user else "receiver"

        return None


class ConversationListSerializer(serializers.ModelSerializer):
    initiator = CustomUserDetailSerializer()
    receiver = CustomUserDetailSerializer()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'initiator', 'receiver', 'last_message']

    def get_last_message(self, instance):
        message = instance.message_set.first()
        if message:
            return MessageSerializer(instance=message, context={'request': self.context.get('request')}).data
        return None


class ConversationSerializer(serializers.ModelSerializer):
    initiator = CustomUserDetailSerializer()
    receiver = CustomUserDetailSerializer()
    message_set = MessageSerializer(many=True)

    class Meta:
        model = Conversation
        fields = ['id', 'initiator', 'receiver', 'message_set']
